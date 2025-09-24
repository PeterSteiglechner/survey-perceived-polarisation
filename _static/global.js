function getLikertLabel(val, lan_en) {
          const numVal = parseInt(val);
          if (lan_en=="True") 
            if (numVal <= -71) return "Strongly Disagree";
            else if (numVal <= -42) return "Disagree";
            else if (numVal <= -13) return "Somewhat Disagree";
            else if (numVal <= 13) return "Neutral";
            else if (numVal <= 42) return "Somewhat Agree";
            else if (numVal <= 71) return "Agree";
            else if (numVal <= 100) return "Strongly Agree";
            else return "NA";
        else
            if (numVal <= -71) return "Stimme überhaupt nicht zu";
            else if (numVal <= -42) return "Stimme nicht zu";
            else if (numVal <= -13) return "Stimme eher nicht zu";
            else if (numVal <= 13) return "Neutral";
            else if (numVal <= 42) return "Stimme eher zu";
            else if (numVal <= 71) return "Stimme zu";
            else if (numVal <= 100) return "Stimme voll und ganz zu";
            else return "NA";
        }
