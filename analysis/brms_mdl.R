# setup
if (!require("pacman")) install.packages("pacman")
pacman::p_load(
    tidyverse, # core wrangling
    brms, # bayesian modeling
    data.table, # data manipulation (optional)
    janitor, # data cleaning (optional)
    here, # reproducible paths (optional)
    bayesplot, # MCMC diagnostics
    posterior, # posterior samples
    loo, # model comparison
)
# install.packages("cmdstanr", repos = c("https://mc-stan.org/r-packages/", getOption("repos")))
# cmdstanr::install_cmdstan()
options(brms.backend = "cmdstanr")
options(mc.cores = parallel::detectCores())
theme_set(theme_minimal())
seed <- 521

# load data
getwd() # perceived-polarization
df <- read_csv("analysis/cleandata/pilot_internal_preprocessed.csv")
colnames(df)
df_with_na <- df[!complete.cases(df), ] # we have one row with na
df <- na.omit(df)

# try to normalize this (min-max)
df <- df %>%
    mutate(
        euclidean_norm = euclideanDistance / max(euclideanDistance, na.rm = TRUE),
        perceived_norm = perceivedDistance / max(perceivedDistance, na.rm = TRUE)
    )

# simple model (varying intercept but not slope)
model_1 <- brm(
    formula = perceived_norm ~ euclidean_norm + (1 | code),
    data = df,
    family = gaussian(),
    prior = c(
        prior(normal(0, 1), class = "Intercept"), # between (-2, +2)
        prior(normal(1, 1), class = "b"), # expect 1-1 mapping.
        prior(exponential(1), class = "sd")
    ),
    chains = 4, iter = 4000, warmup = 2000, cores = 4, seed = seed,
    control = list(adapt_delta = 0.99, max_treedepth = 20)
)

# simple model (varying intercept + slopes)
model_2 <- brm(
    formula = perceived_norm ~ euclidean_norm + (1 + euclidean_norm | code),
    data = df,
    family = gaussian(),
    prior = c(
        prior(normal(0, 1), class = "Intercept"),
        prior(normal(1, 1), class = "b"),
        prior(exponential(1), class = "sd"),
        prior(lkj(2), class = "cor") # for correlation between intercept and slope
    ),
    chains = 4, iter = 4000, warmup = 2000, cores = 4, seed = seed,
    control = list(adapt_delta = 0.99, max_treedepth = 20)
)

# compare models with loo()
loo_1 <- loo(model_1)
loo_2 <- loo(model_2)
loo_compare(loo_1, loo_2)

# model 2 is preferred (but uncertain)
# elpd_diff: expected log predictive density difference (out-of-sample pred. acc.)
# se_diff: how uncertain elpd_diff is (standard error: so here uncertain)

# visualize

# Add fitted values to the data
df_fitted <- df %>%
    mutate(
        fitted_model1 = fitted(model_1)[, "Estimate"],
        fitted_model2 = fitted(model_2)[, "Estimate"]
    )

# Sample a few participants for clarity (change n as needed)
sampled_codes <- sample(unique(df$code), 9)

p <- df_fitted %>%
    filter(code %in% sampled_codes) %>%
    pivot_longer(cols = starts_with("fitted_model"), names_to = "model", values_to = "fitted") %>%
    ggplot(aes(x = euclidean_norm, y = perceived_norm)) +
    geom_point(alpha = 0.6, size = 2) +
    geom_line(aes(y = fitted, color = model)) +
    facet_wrap(~code, nrow = 3) +
    scale_color_manual(values = c("fitted_model1" = "gray40", "fitted_model2" = "steelblue")) +
    labs(
        title = "Observed vs Fitted Perceived Distances",
        subtitle = "Random intercept vs intercept + slope models",
        x = "Euclidean Distance",
        y = "Perceived Distance",
        color = "Model"
    ) +
    theme_minimal(base_size = 14) +
    theme(
        legend.position = "bottom",
        strip.text = element_text(size = 12),
        plot.title = element_text(size = 16, face = "bold"),
        plot.subtitle = element_text(size = 12)
    )

# Save it — you can scale however you like
ggsave(
    "analysis/figs/id_fits.png",
    plot = p,
    width = 6,
    height = 6,
    dpi = 300,
    bg = "white"
)

### plot 2 ###

# A grid of X values from 0 to 1 (normalized scale)
new_data <- tibble(
    euclidean_norm = seq(0, 1, length.out = 100),
    code = NA # force population-level prediction (not per participant)
)
# Get population-level predictions (marginal over random effects)
fit1 <- fitted(model_1, newdata = new_data, re_formula = NA) %>% as_tibble()
fit2 <- fitted(model_2, newdata = new_data, re_formula = NA) %>% as_tibble()

# Combine with prediction grid and tag model
pop_preds <- bind_rows(
    bind_cols(new_data, fit1) %>% mutate(model = "model_1"),
    bind_cols(new_data, fit2) %>% mutate(model = "model_2")
)

p2 <- ggplot(pop_preds, aes(x = euclidean_norm, y = Estimate, color = model, fill = model)) +
    geom_line() +
    geom_ribbon(aes(ymin = Q2.5, ymax = Q97.5), alpha = 0.2, color = NA) +
    scale_color_manual(values = c("model_1" = "gray40", "model_2" = "steelblue")) +
    scale_fill_manual(values = c("model_1" = "gray40", "model_2" = "steelblue")) +
    labs(
        title = "Population-Level Prediction",
        subtitle = "Mean and 95% credible interval",
        x = "Euclidean Distance (normalized)",
        y = "Perceived Distance (normalized)",
        color = "Model",
        fill = "Model"
    ) +
    theme_minimal(base_size = 14) +
    theme(
        legend.position = "bottom",
        plot.title = element_text(size = 16, face = "bold"),
        plot.subtitle = element_text(size = 12)
    ) +
    geom_point(data = df, aes(x = euclidean_norm, y = perceived_norm), inherit.aes = FALSE, alpha = 0.1)

ggsave(
    "analysis/figs/pop_fits.png",
    plot = p2,
    width = 4,
    height = 4,
    dpi = 300,
    bg = "white"
)

## explore random effects ##
ranef(model_2) # subject-specific intercepts/slopes (with CIs)
coef(model_2) # subject-specific values (fixed + random effects)

# more complex models #
# model 3 (just random intercept here?)
colnames(df)
model_3 <- brm(
    formula = perceived_norm ~ d_climate_concern + d_gay_adoption + d_migration_enriches_culture + d_govt_reduce_inequ + (1 | code),
    data = df,
    family = gaussian(),
    prior = c(
        prior(normal(0, 1), class = "Intercept"), # between (-2, +2)
        prior(normal(0, 1), class = "b"), # here lower than before (center at 0 for now)
        prior(exponential(1), class = "sd")
    ),
    chains = 4, iter = 4000, warmup = 2000, cores = 4, seed = seed,
    control = list(adapt_delta = 0.99, max_treedepth = 20)
)

# compare model 3 to the simpler models
loo_3 <- loo(model_3)
loo_compare(loo_1, loo_2, loo_3) # model 3 is terrible.

# look at fixed effects
fixef(model_1) # reasonable: basically 1-1 mapping
fixef(model_2) # reasonable: basically 1-1 mapping (intercept positive: so when no actual distance, perceive some distance)
fixef(model_3) # This looks weird though (should all be positive). Also intercept becomes larger here.

## plot model 3 ##
pp_check(model_3)

library(bayesplot)
mcmc_areas(as_draws_df(model_3), pars = vars(starts_with("b_")))

df$pred_model3 <- fitted(model_3)[, "Estimate"]

ggplot(df, aes(x = pred_model3, y = perceived_norm)) +
    geom_point(alpha = 0.3) +
    geom_abline(intercept = 0, slope = 1, linetype = "dashed", color = "gray") +
    labs(
        x = "Predicted perceived distance (model_3)",
        y = "Observed perceived distance",
        title = "Predicted vs Observed (Model 3)"
    ) +
    theme_minimal()

library(bayesplot)
mcmc_areas(as_draws_df(model_3), pars = vars(starts_with("b_")))
