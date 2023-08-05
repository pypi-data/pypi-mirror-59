# gym-display-advertising

An OpenAI Gym for Shopping Cart Reinforcement Learning.

This is a project by [Winder Research](https://WinderResearch.com), a Cloud-Native Data Science consultancy.

## Installation

`pip install gym-shopping-cart`

## Usage

This example will use the small example data included in the repo.

```python
import gym
import gym_shopping_cart

env = gym.make("ShoppingCart-v0")
episode_over = False
rewards = 0
while not episode_over:
    state, reward, episode_over, _ = env.step(env.action_space.sample())
    print(state, reward)
    rewards += reward
print("Total reward: {}".format(rewards))
```

## Real Shopping Cart Data

This environment uses real shopping cart information from the [Instacart dataset](https://tech.instacart.com/3-million-instacart-orders-open-sourced-d40d29ead6f2).

To help read this data the library also comes with a data parser. This loads the raw data and cleans the data to be in a format expected by the environment.

## Credits

Gitlab icon made by [Freepik](https://www.flaticon.com/authors/freepik) from [www.flaticon.com](https://www.flaticon.com/).
