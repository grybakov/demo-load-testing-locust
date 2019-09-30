# Demo: Load test with Locust

Demo load test written for the Q&A service [Toster](https://toster.ru).

![demo load testing](demo-screen.gif "Demo: Load test with Locust")

## Workload model
Workload modeling identifies some workload profiles to be simulated against the tested application.

### User of search
  - User searches for posts on specific topics (success)
  - User searches for posts (failure)

### User of topic
  - User views top, new and unanswered posts

### Random user
  - User views random pages
  - User views random pages and random posts

## Requirements

  - [locust](https://locust.io/)
  - [pyquery](https://github.com/gawel/pyquery)