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


 // Function to get color styling based on answer value
  function getAnswerStyling(answer) {
      const label = getLikertLabel(answer, "{{lan_en}}");
      const trimmedAnswer = label.toLowerCase().trim();
      let backgroundColor = '';
      let texcolor = "black";

      if (trimmedAnswer === 'strongly disagree' || trimmedAnswer === 'stimme überhaupt nicht zu') {
          backgroundColor = 'rgba(220, 53, 69, 1)'; // deep red
          texcolor = "rgb(255, 255, 255)";
      } else if (trimmedAnswer === 'disagree' || trimmedAnswer === 'stimme nicht zu') {
          backgroundColor = 'rgba(255, 99, 132, 0.9)'; // medium red
          texcolor = "rgb(255, 255, 255)";
      } else if (trimmedAnswer === 'somewhat disagree' || trimmedAnswer === 'stimme eher nicht zu') {
          backgroundColor = 'rgba(255, 178, 102, 0.8)'; // orange-red
      } else if (trimmedAnswer === 'neutral' || trimmedAnswer === 'teils/teils') {
          backgroundColor = 'rgba(201, 203, 207, 0.6)'; // light gray
      } else if (trimmedAnswer === 'somewhat agree' || trimmedAnswer === 'stimme eher zu') {
          backgroundColor = 'rgba(144, 238, 144, 0.8)'; // light green
      } else if (trimmedAnswer === 'agree' || trimmedAnswer === 'stimme zu') {
          backgroundColor = 'rgba(60, 179, 113, 0.9)'; // medium green
          texcolor = "rgb(255, 255, 255)";
      } else if (trimmedAnswer === 'strongly agree' || trimmedAnswer === 'stimme voll und ganz zu') {
          backgroundColor = 'rgba(40, 167, 69, 1)'; // deep green
          texcolor = "rgb(255, 255, 255)";
      } else {
          backgroundColor = 'rgba(161, 161, 161, 1)'; // grey
          texcolor = "rgba(0, 0, 0, 1)";
      }

      return backgroundColor
          ? `background-color: ${backgroundColor}; color: ${texcolor}; padding: 4px 0px; border-radius: 0px;`
          : '';
  }