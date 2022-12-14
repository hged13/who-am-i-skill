# <img src="https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/robot.svg" card_color="#22A7F0" width="50" height="50" style="vertical-align:bottom"/> Who Am I
This skill trains a classification model on the first call. Then, it performs voice classification and pulls user data out of stored csv files. This skill is dependent on the New-User-Creation-Skill, and must be reinstalled if the former skill is added to so that the classification model will be retrained to include an added user. 

## About
- After imaging your Pi's sd card with the most recent Picroft image...
- Install this skill thorugh the command    mycroft-msm install https://github.com/hged13/who-am-i-skill
- All dependencies will be installed upon installation of this skill
- THIS DOES NOT INCLUDE INSTALLATION OF THE New-User-Creation-Skill which MUST be installed and must include at least TWO profiles in order for this skill to function properly.
- The user speaks "Classify me" and the pi will take a 5 second audio sample
- This will be run through the prediction model and a user name will be identified
- Upon confirmation, or override ("No this is -your name-) you can ask the speaker to "play my radio" "play my playlist" or "play my artist"



## Examples
* "Classify me"

## Credits
Hged13

## Category
**Music & Audio**

## Tags

