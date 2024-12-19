# D&D Assistant

## Overview

D&D Assistant is an AI-powered tool designed to enhance the Dungeons & Dragons gaming experience. Utilizing the Llama 3.1 model and the Cerebras API for ultra high-speed inference, it acts as a dynamic Dungeon Master, managing game states, responding to player actions, and facilitating an interactive storytelling environment.

## Features

- **Dynamic Game State Management**: Tracks player stats, enemies, items, and locations.
- **AI-Powered Responses**: Generates contextual and coherent responses based on the current game state.
- **Extensible Data Structures**: Easily add new enemies, items, and locations via JSON files.
- **Interactive CLI**: Simple command-line interface for engaging with the game.
- **Game Reset Functionality**: Reset the game to its initial state at any time for consistent starting points.

### Prerequisites

- **Python 3.9+**
- **Git**
- **A Cerebras API key**

### Sample Use

```Narrative: Varric the Vigilant stands at the edge of a dense forest clearing, his rusty sword gleaming faintly in the sunlight. The air is thick with the scent of pine and earth. Suddenly, a Goblin Grunt emerges from the shadows, eyeing Varric warily.```

Response: attack

`Narrative: Varric the Vigilant swings his rusty sword at the Goblin Grunt, striking it with force. The goblin recoils, losing 5 HP.`

Response: drink potion

`Narrative: Varric the Vigilant drinks the health potion from his inventory, feeling a warm sensation spread through his body. His health increases by 10 HP.`

Response: investigate cave

`Narrative: Varric the Vigilant moves cautiously towards the dark cave. The sounds of dripping water grow louder as he approaches, and the shadows seem to dance ominously.`