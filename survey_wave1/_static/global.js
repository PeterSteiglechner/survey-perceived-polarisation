function getLikertLabel(val, lan_en) {
          const numVal = parseInt(val);
          if (lan_en=="True") 
            if (numVal <= -990) return "Prefer not to say"; 
            else if (numVal <= -71) return "Strongly Disagree";
            else if (numVal <= -42) return "Disagree";
            else if (numVal <= -13) return "Somewhat Disagree";
            else if (numVal <= 13) return "Neutral";
            else if (numVal <= 42) return "Somewhat Agree";
            else if (numVal <= 71) return "Agree";
            else if (numVal <= 100) return "Strongly Agree";
            else return "NA";
        else
            if (numVal <= -990) return "Keine Angabe"; 
            else if (numVal <= -71) return "Stimme überhaupt nicht zu";
            else if (numVal <= -42) return "Stimme nicht zu";
            else if (numVal <= -13) return "Stimme eher nicht zu";
            else if (numVal <= 13) return "Neutral";
            else if (numVal <= 42) return "Stimme eher zu";
            else if (numVal <= 71) return "Stimme zu";
            else if (numVal <= 100) return "Stimme voll und ganz zu";
            else return "NA";
        }


// Function to get color styling based on answer value
function getAnswerStyling(answer) {
  const label = getLikertLabel(answer, "{{lan_en}}");
  const trimmedAnswer = label.toLowerCase().trim();
  let backgroundColor = '';
  let texcolor = "black";
  
  if (trimmedAnswer === 'prefer not to say' || trimmedAnswer === 'keine angabe') {
    backgroundColor = 'rgba(255, 255, 255, 1)'; // deep red
    texcolor = "rgba(148, 148, 148, 1)";
  } else if (trimmedAnswer === 'strongly disagree' || trimmedAnswer === 'stimme überhaupt nicht zu') {
    backgroundColor = 'rgba(183, 28, 28, 1)'; // deep red
    texcolor = "rgb(255, 255, 255)";
  } else if (trimmedAnswer === 'disagree' || trimmedAnswer === 'stimme nicht zu') {
    backgroundColor = 'rgba(229, 57, 53, 1)'; // medium red
    texcolor = "rgb(255, 255, 255)";
  } else if (trimmedAnswer === 'somewhat disagree' || trimmedAnswer === 'stimme eher nicht zu') {
    backgroundColor = 'rgba(239, 154, 154, 1)'; // light red
  } else if (trimmedAnswer === 'neutral' || trimmedAnswer === 'teils/teils') {
    backgroundColor = 'rgba(224, 224, 224, 1)'; // neutral gray
  } else if (trimmedAnswer === 'somewhat agree' || trimmedAnswer === 'stimme eher zu') {
    backgroundColor = 'rgba(129, 199, 132, 1)'; // light green
  } else if (trimmedAnswer === 'agree' || trimmedAnswer === 'stimme zu') {
    backgroundColor = 'rgba(56, 142, 60, 1)'; // medium green
    texcolor = "rgb(255, 255, 255)";
  } else if (trimmedAnswer === 'strongly agree' || trimmedAnswer === 'stimme voll und ganz zu') {
    backgroundColor = 'rgba(27, 94, 32, 1)'; // deep green
    texcolor = "rgb(255, 255, 255)";
  } else {
    backgroundColor = 'rgba(161, 161, 161, 1)'; // grey
    texcolor = "rgba(0, 0, 0, 1)";
  }

      return backgroundColor
          ? `background-color: ${backgroundColor}; color: ${texcolor}; padding: 4px 0px; border-radius: 0px;`
          : '';
  }