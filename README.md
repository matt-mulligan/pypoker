# PyPoker

Version - 0.1.0

Author - Matt Mulligan

Python poker logic engine and game runner.

I'm an avid poker player in real life and thought it would be fun/challenging to implement a poker logic engine myself.

## Project Goals
I have a number of goals/milestones I wish to add to PyPoker. Below I have listed the main functionality I wish to introduce over time.

 - Implement basic engine.hand_logic package
    - Utilises ABC with an implementation for each poker game type (Texas Holdem, Pineapple, Omaha, etc)
    - implement public method for finding a players best possible hand
    - implement public method for ranking players hands against each other
    - implement public method for determining each players odds of winning
 - Implement basic engine.game_runner package
    - Utilises ABC with an implementation for each poker game type (Texas Holdem, Pineapple, Omaha, etc)
    - Runs a game session for local players (same computer to start with)
    - manages betting, turn action, winner/loser, etc
    - initially accessible/playable via cmd line inputs
 - Extend game_runner to play via a GUI
 - Extend game_runner to log results to some datastore for analysis
 - Extend game_runner to have a server/client interface for remote play
 - Add a basic computer opponent using a logic engine
 - Add a much more advanced player using machine learning

## Version/Product Information 
Version information is maintained within the docs/version_history.md file of the repository


## Development Info:
Below is useful information to how I have structured the project
 - Minimum Python Version = 3.8
 - Branching Model = [GitFlow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
 - Environment/Package Management = [Poetry](https://python-poetry.org/) - configuration within the pyproject.toml file
 - Testing Framework = [PyTest](https://docs.pytest.org/en/stable/) & [PyTest-BDD](https://pytest-bdd.readthedocs.io/en/latest/)
 - Testing Types = Unit Tests & Functional Tests
 - CICD Pipelines
     - Github Actions
     - Pipeline triggered on any PR to develop or master
     - Actions
        - build environment (unix)
        - install dependencies using poetry (py 3.8)
        - run black code check
        - run unit test suite
        - run functional test suite
        - publish results
