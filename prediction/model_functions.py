import pandas as pd
import numpy as np
import time 

from scipy.spatial import distance_matrix


def inferSubjectiveLenses(df, parties, waves, variables):
    """
    Extract the subjective lenses (matrices containing the scaled and rotated axes) for each partisan identity-group from opinion data in different waves.
    
    Parameters:
        df (pd.DataFrame): Dataframe containing the columns "essround", "identity", and those listed in variables.
        parties (list): List containing the parties.
        waves (list): List of the waves (values in df.essround).
        variables (list): List of the opinion columns.
    
    Returns:
        dict: a transofrmation matrix for each wave and party.
    """
    LensTransformation = {}
    
    for r in waves:
        # (1) Lens without considering identites (identity group "None")
        X = df.loc[df.essround == r, variables].dropna(how="any", axis="index").to_numpy()
        eigval, evec = np.linalg.eig(np.cov(X.T))   # returns w, v: column v[:,i] is the eigenvector corresponding to the  eigenvalue w[i]
        LNone = np.array([eigval[ni]**0.5 * evec[:, ni] for ni, i in enumerate(range(np.cov(X.T).shape[0]))]).T
        LNoneinv = np.linalg.inv(LNone)
        LensTransformation[r] = {"None": np.dot(LNoneinv.T, LNoneinv)}
        
        # (2) Lenses for each partisan group
        for p in parties:
            if not (p == "None"):
                X_p = df.loc[(df.essround == r) & (df.identity == p), variables].dropna(how="any", axis="index").to_numpy()
                if not len(X_p) == 0:
                    eigval, evec = np.linalg.eig(np.cov(X_p.T))
                    L_p = np.array([eigval[ni]**0.5 * evec[:, ni] for ni, i in enumerate(range(np.cov(X_p.T).shape[0]))]).T
                    if len(variables) > 1:
                        assert np.dot(L_p[:, 0], L_p[:, 1]) < 1e-13
                    #arrows of the coordinate system [r][p] = L_p
                    L_p_inv = np.linalg.inv(L_p)
                    LensTransformation[r][p] = np.dot(L_p_inv.T, L_p_inv)
    
    return LensTransformation




def subjectiveDistanceMatrix(opinions_observer, opinions_observed, ids_observer, Lenses):
    """
    Calculate the subjective pairwise distance matrix.
    
    Parameters:
        opinions_observer (np.ndarray): N x M opinion vector of N observers.
        opinions_observed (np.ndarray): K x M opinion vector of K observed individuals.
        ids_observer (list): Length N vector containing the identities of the observers.
        currLenses_set (dict): Dictionary of the lens transformation matrices (M x M) used by each identity group.
    
    Returns:
        np.ndarray: Subjective pairwise squared distance matrix.
    """
    subj_dist_matrix = np.empty((len(ids_observer), len(opinions_observed)))
    for ni, (id_i, op_i) in enumerate(zip(ids_observer, opinions_observer)):
        D = Lenses[id_i]
        d = opinions_observed - op_i  # distance vector from observer i
        subj_dist_matrix[ni, :] = np.sum(np.dot(d, D) * d, axis=1)**(1/2) # sum over the M topics
    
    return subj_dist_matrix


def avg_distances(dist_matrix, w_obs=None, w_obd=None, all_observe_all=False):
    """
    Average over the pairwise distance matrix with weights.
    
    Parameters:
        dist_matrix (np.ndarray): Pairwise distance matrix of shape N x K.
        w_obs (np.ndarray): N x 1 array containing the weights of the observers.
        w_obd (np.ndarray): K x 1 array containing the weights of the observed individuals.
        all_observe_all (bool): If True, the normalising constant is (sum(w)-1); if False, sum(w) where w are the weights of the observed individuals.
    
    Returns:
        float: Averaged distance/disagreement index.
    """
    if dist_matrix.shape[1] == 1:  
        # single observer --> no averaging.
        return dist_matrix
    
    # Define weights if w_obs=w_obd=None
    if w_obs is None and w_obd is None:
        w_obs = np.ones(dist_matrix.shape[0])
        w_obd = np.ones(dist_matrix.shape[1])
    
    # Normalise weights  
    # ... for observer w_i / sum_k(w_k)
    w_obs_norm = w_obs / w_obs.sum()
    # ... for observed w_i / (sum_k(w_k)-w_i)  if observer i is included in the observed
    w_obd_norm = w_obd / (w_obd.sum() - w_obd) if all_observe_all else w_obd / w_obd.sum()
    
    # d_mean = w^T * Distance_Matrix * w 
    avg = np.dot(w_obs_norm.T, np.dot(dist_matrix, w_obd_norm))
    # dimensions: [[1 x N] * [N x K] * [K x 1] = [1,1]]
    
    return avg



def calc_meanPerceivedDisagreement(df, waves, variables, Lenses):   
    """
    Calculate mean perceived disagreement from the opinion data at different waves using different subjective lenses.
    
    Parameters:
        df (pd.DataFrame): Dataframe that contains the columns "essround", "identity", and those listed in variables
        waves (list): List of waves (values in df.essround)
        variables (list): List of opinion columns.
        Lenses (dict): Dictionary of the lens transformation matrices (M x M) used by each identity group.
        
    Returns:
        dict: Perceived mean distances for each wave and for each set of lens transformation matrices used.
    """
    mean_d = dict(zip(waves, [{} for _ in waves]))
    
    for n, r in enumerate(waves):
        df_wave = df.loc[df.essround == r,:]
        for C in waves[:n+1]:
            obs = df_wave
            obd = df_wave
            ids = df_wave["identity"]
            subjDistMatrix = subjectiveDistanceMatrix(obs[variables].to_numpy(), obd[variables].to_numpy(), ids, Lenses[C])
            mean_d[r][C] = avg_distances(subjDistMatrix, obs.anweight, obd.anweight, True)
    return mean_d


def calc_meanObjectiveDisagreement(data, waves, variables):
    """
    Calculate mean objective disagreement from the opinion data at different waves.
    
    Parameters:
        df (pd.DataFrame): Dataframe that contains the columns "essround", "identity", and those listed in variables
        waves (list): List of waves (values in df.essround)
        variables (list): List of opinion columns.
        
    Returns:
        dict: Objective mean distances for each wave.
    """
    Aobjmd = {}
    for r in waves:
        df = data.loc[data.essround==r, :]
        obs = df
        Aobjd = distance_matrix(obs[variables].to_numpy(), obs[variables].to_numpy())
        Aobjmd[r] = avg_distances(Aobjd, obs.anweight, obs.anweight, True)
    return Aobjmd


def calc_meanPerceivedDisagreement_betweenGroups(df, waves, parties, variables, Lenses):
    """
    Calculate mean perceived disagreement from opinion data between waves as seen by the different parties.
    
    Parameters:
        df (pd.DataFrame): Dataframe that contains the columns "essround", "identity", and those listed in variables
        waves (list): List of waves.
        parties (list): List of parties.
        variables (list): List of opinion columns.
        Lenses (dict): Dictionary of lens transformation matrices for each wave and party.
    
    Returns:
        pd.DataFrame: Mean average opinion distance for each wave and each set of lens transformation matrices as seen by each partisan identity group (PxA_meanDist).
        pd.DataFrame: Mean average opinion distance to each group for each wave and each set of lens transformation matrices as seen by each partisan identity group (PxP_meanDist).
    """
    
    PxA_meanDist = dict(zip(waves, [dict(zip(waves, [{} for _ in waves])) for _ in waves]))
    PxP_meanDist = dict(zip(waves, [dict(zip(waves, [{} for _ in waves])) for _ in waves]))
    
    for n, party_obs in enumerate(parties):
        print(f"{party_obs}")
        p_obs_k = party_obs[0].lower()
        for n, r in enumerate(waves):
            s0 = time.time()
            print(f"wave {r}", end="  ")
            df_wave = df.loc[df.essround == r, :]
            obs = df_wave.loc[df_wave.identity == party_obs]
            for C in waves[:n+1]:
                for party_obd in parties: 
                    p_obd_k = party_obd[0].lower()
                    # does the observer group "observe" themselves? 
                    AoA = True if party_obd == party_obs else False  
                    obd = df_wave.loc[df_wave.identity == party_obd]
                    
                    # PxP: party-by-party
                    PxP_d = subjectiveDistanceMatrix(obs[variables].to_numpy(), obd[variables].to_numpy(), obs.identity, Lenses[C])
                    PxP_meanDist[r][C][p_obs_k + p_obd_k] = avg_distances(PxP_d, w_obs=obs.anweight, w_obd=obd.anweight, all_observe_all=AoA)

                # PxA: party-to-all
                obd = df_wave
                PxA_d = subjectiveDistanceMatrix(obs[variables].to_numpy(), obd[variables].to_numpy(), obs.identity, Lenses[C])
                PxA_meanDist[r][C][p_obs_k] = avg_distances(PxA_d, w_obs=obs.anweight, w_obd=obd.anweight, all_observe_all=True)

            print(f"--> done ({(time.time() - s0):.0f} seconds, n={len(obs)})")
            
    PxA_meanDist_df = {}
    for opinionwave, percDist_bywave in PxA_meanDist.items():
        for lenswave, percDist in percDist_bywave.items():
            if not percDist_bywave[lenswave]=={}:
                PxA_meanDist_df[(opinionwave,lenswave)] = percDist
    PxA_meanDist_df = pd.DataFrame(PxA_meanDist_df)

    PxP_meanDist_df = {}
    for opinionwave, percDist_bywave in PxP_meanDist.items():
        for lenswave, percDist in percDist_bywave.items():
            if not percDist_bywave[lenswave]=={}:
                PxP_meanDist_df[(opinionwave,lenswave)] = percDist
    PxP_meanDist_df = pd.DataFrame(PxP_meanDist_df)
    PxP_meanDist_df["obs"] = PxP_meanDist_df.apply(lambda x: x.name[0], axis=1)
    PxP_meanDist_df["obd"] = PxP_meanDist_df.apply(lambda x: x.name[1], axis=1)    
    return PxA_meanDist_df, PxP_meanDist_df
