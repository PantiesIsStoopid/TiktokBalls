# Bouncing Balls Simulation with Sound Effects

This Python application uses **Pygame** to simulate balls bouncing within a circular boundary, featuring **no loss of energy** during collisions and playing a sound effect upon collision.

## Features

- **Random number of balls** (between 1 and 6) generated for each run.
- Balls have:
  - Random **velocity** and **direction**.
  - Random color from a **rainbow palette**.
- **No loss of momentum**: Balls maintain energy during collisions.
- Collision detection:
  - Between balls and the **circular boundary**.
  - With the **window edges** (walls).
- **Collision sounds** play upon each collision.
- The simulation is recorded as a **60-second video** and saved as `bouncing_balls_with_sound.avi`.

## Libraries Used

- `pygame`: Used for creating the graphical interface, drawing shapes, handling collisions, and playing sounds.
- `numpy`: Used for handling frame transformations during video recording.
- `opencv-python (cv2)`: Used to record and save the video of the simulation.

## Installation

Ensure you have Python and the required libraries installed:

```bash
pip install pygame numpy opencv-python
```