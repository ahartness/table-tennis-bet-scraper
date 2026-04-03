# Table Tennis Scraper

## TODO Items:
- [ ] Break out into individual components
    - [ ] Bar Chart component
    - [ ] Button Component
    - [X] Utils for date function and others
- [ ] Win/Loss Expectations or Predictions
- [ ] 1st Set Point Spread odds (Always ±2.5)
- [ ] Set 1 & 2 or Set 2 & 3 
- [X] Try catch added to python script incase it fails on docker container
- [X] Add more data to bar chart on visual nodejs UI
- [ ] Add Data Tables under Bar Chart to show a more indepth breakdown of stats
- [ ] Styling updates / Maybe use Figma for prototyping
- [X] Date Time check to only pull games that are not started
- [X] Automate the script and push to github for the UI Visualizer
  - [ ] Need to push this to a Docker Container
- [ ] Build out different way of selecting games (dropdown can feel cramped)
- [ ] Pulling Over/Under Lines from Sportsbook to increase/decrease target depending on match-up

## Future Updates;
- [ ] Pull Data for other sports (Hockey/NFL/NBA)

## Possible Future Uptades
- [ ] Make a Private instance on Home Server (Need to buy a NAS for this)
- [ ] Mobile App?

## Completed Items
- [X] Send push notifications when there is an upcoming game
- [X] Investigate scores24 graphql endpoints
- [X] Create a new script that uses scores24.live since there's more game data there
- [X] Create variables for all editable fields
- [X] Get Last "X" and full percentages to csv file
- [X] Need weights added to the records based on games played
- [X] Update algorithm for what are the best plays to show
- [X] Fine Tune the Bet Amount for the "Best Plays"
- [X] Logging updates for the output file doesn't become too large
  - [X] Using Docker for this instead
- [X] Create a visual & interactive UI (NextJS or Angular) -- Do Another Time

## Running with docker

```
docker build -t table-tennis-scraper .
```

Next Kill the old container

```
docker container kill <container_name>

docker container rm <container_name>
```

Next:  Start the new container from latest image
```
docker run -d --name=<worker-name-here> <image_name>:latest
```

Next:  View Logs to Validate
```
docker logs <container_name>
```

Run terminal shell inside docker container:
```
docker exec -it <container_name> sh
```
