function getLikertLabel(val, lan_en) {
          const numVal = parseInt(val);
          if (lan_en=="true") 
            if (numVal <= -71) return "Strongly Disagree";
            else if (numVal <= -42) return "Disagree";
            else if (numVal <= -13) return "Somewhat Disagree";
            else if (numVal <= 13) return "Neutral";
            else if (numVal <= 42) return "Somewhat Agree";
            else if (numVal <= 71) return "Agree";
            else return "Strongly Agree";
        else
            if (numVal <= -71) return "Stimme überhaupt nicht zu";
            else if (numVal <= -42) return "Stimme nicht zu";
            else if (numVal <= -13) return "Stimme eher nicht zu";
            else if (numVal <= 13) return "Neutral";
            else if (numVal <= 42) return "Stimme eher zu";
            else if (numVal <= 71) return "Stimme zu";
            else return "Stimme voll und ganz zu";
        }
