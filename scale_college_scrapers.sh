#!/bin/bash

# Function to scale dynos
scale_dynos() {
  APP_NAME=$1
  ACTION=$2
  DYNO_TYPE=$3
  QUANTITY=$4

  case $ACTION in
    scale-up)
      echo "Scaling up $DYNO_TYPE dynos to $QUANTITY for app $APP_NAME..."
      heroku ps:scale $DYNO_TYPE=$QUANTITY -a $APP_NAME
      ;;
    
    scale-down)
      echo "Scaling down $DYNO_TYPE dynos to $QUANTITY for app $APP_NAME..."
      heroku ps:scale $DYNO_TYPE=$QUANTITY -a $APP_NAME
      ;;
    
    *)
      echo "Invalid action. Use 'scale-up' or 'scale-down'."
      exit 1
      ;;
  esac

  echo "Done!"
}

# Scale up or down for both apps
ACTION=$1
DYNO_TYPE=web

if [ "$ACTION" == "scale-up" ]; then
  QUANTITY=1
elif [ "$ACTION" == "scale-down" ]; then
  QUANTITY=0
else
  echo "Invalid action. Use 'scale-up' or 'scale-down'."
  exit 1
fi

# Scale for college-scraper-api
scale_dynos "college-scraper-api" $ACTION $DYNO_TYPE $QUANTITY

# Scale for college-scraper-frontend
scale_dynos "college-scraper-frontend" $ACTION $DYNO_TYPE $QUANTITY
