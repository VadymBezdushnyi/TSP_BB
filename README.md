# Travelling Salesman Problem solver with Branch-And-Bound technique

# Description
## Algorithm

Algorithm accepts weight matrix NxN and finds path which visits all nodes and has minimal total weight.
For detailed explanation please visit https://www.geeksforgeeks.org/traveling-salesman-problem-using-branch-and-bound-2/
For visualization purposes not only optimal, but all matrices are saved.
Algorithm is implemented inside TSPMatrix.py and TSPSolver.py classes 
For matrix operations numpy is used, however algorithm is relatively slow, because every step is saved for visualization

Algorithm has some low-level development testing which can be found in `TestRunner.py`(never runs on cloud)

## Website
Simple Flask app is created, app has only two endpoints : `/` for web-page and `/calculate` for matrix calculation
Explore `TSPServer.py` for more details.

## Interface & Visalization

Web page has simple structure with 3 components:
- Matrix input with test samples
- Solution visualization
- Solver animation

Frontend is located inside `static/` and `templates/` folders

Frontend is tested using Selenium tests


# Build and testing
## Manual build

To test locally clone project, then:
- install python3.8 and pip3 using official instructions
- install requirements `pip3 install -r requirements.txt` 
- Run web app `python3 -m flask run --host=0.0.0.0`
- (Optionally) Run selenium tests on it

## Using Docker

Alternatively you can use Docker to run application.
The latest version can be installed and run with
```
docker run vadymbezdushnyi/tsp-bb:latest
```

Each commit to master creates new docker image.  
Visit `.github/workflows` to explore more details.  

## Using Demo on Heroku

View demo here: https://tsppy.herokuapp.com/