### ENGINE ###
UPDATE_PERIOD_MS = 5
DRAW_PERIOD_MS = 15

### WINDOW ###
WINDOW_SIZE = (400, 625)

### GRAPHICS ###
SPRITE_PATH = "sprite/"
SPACESHIP_SPRITE_NAME = "spaceship.png"
ALIEN_SPRITE_NAMES = [
    ["alien1_frame1.png", "alien1_frame2.png"],
    ["alien2_frame1.png", "alien2_frame2.png"],
    ["alien3_frame1.png", "alien3_frame2.png"]
]
ALIEN_EXPLOSION_SPRITE_NAME = "alien_explosion.png"
MISSILE_EXPLOSION_SPRITE_NAME = "missile_explosion.png"
SPACESHIP_SPRITE_NAME = "spaceship.png"
LASER_SPRITE_NAMES = [
    ["laser1_frame1.png", "laser1_frame2.png", "laser1_frame3.png", "laser1_frame4.png"],
    ["laser2_frame1.png", "laser2_frame2.png", "laser2_frame3.png", "laser2_frame4.png"],
    ["laser3_frame1.png", "laser3_frame2.png", "laser3_frame3.png", "laser3_frame4.png"]
]
LASER_EXPLOSION_SPRITE_NAME = "laser_explosion.png"
SPACESHIP_DESTRUCTION_SPRITE_NAME = "spaceship_explosion.png"
BARRICADE_SPRITE_NAME = "barricade.png"
SAUCER_SPRITE_NAME = "saucer.png"
SAUCER_EXPLOSION_SPRITE_NAME = "saucer_explosion.png"

### SOUND ###
SOUND_PATH = "sound/"
ALIEN_DESTROYED_SOUND = "alien_destroyed.wav"
ALIEN_MOVE_SOUNDS = [
    "invader_movements1.wav",
    "invader_movements2.wav",
    "invader_movements3.wav",
    "invader_movements4.wav",
    "invader_movements5.wav",
    "invader_movements6.wav"
]
SPACESHIP_SHOOT_SOUND = "shoot.wav"
SPACESHIP_DESTRUCTION_SOUND = "explosion.wav"
SAUCER_SOUND = "saucer.wav"
SAUCER_DESTRUCTION_SOUND = "saucer_destroyed.wav"

ONE_LIFE_UP_SOUND = "one_life.wav"

### ENTITIES ###
WORLD_DIM = (400, 600)

### LIFE_COUNT ###
STARTING_LIFE_COUNT = 3
LIFE_COUNT_POS = (WORLD_DIM[0] // 20, WORLD_DIM[1] + 3)
LIFE_POS = (WORLD_DIM[0] // 10, WORLD_DIM[1] + 3)
LIFE_POS_SHIFT = (3, 0)
ONE_LIFE_SCORE = 1500

### SPACE_SHIP ###
SPACESHIP_STARTING_POSITION = (WORLD_DIM[0] // 2, WORLD_DIM[1] * 9 // 10)
SPACESHIP_SPEED_PIXEL_PER_SECOND = 100
SPACESHIP_EXPLOSION_DURATION_MS = 1000

### MISSILE ###
MISSILE_RECT_DIM = (2, 6)
MISSILE_RECT_COLOR = (0, 255, 0)
MISSILE_SPEED_PIXEL_PER_SECOND = 500

### ALIENS ###
ALIEN_FORMATION = [
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
ALIEN_FORMATION_WIDTH_PIXELS = 344
ALIEN_SPEED_PIXEL_PER_SECOND = 10
ALIEN_FIRING_PERIOD_MS = 1000
ALIEN_SPRITE_SHIFT_PERIOD_MS = 500
ALIEN_STARTING_POS_Y = WORLD_DIM[1] * 3 // 10
ALIEN_EXPLOSION_DURATION_MS = 250

### SAUCER ###
SAUCER_SPEED_PIXEL_PER_SECOND = 100
SAUCER_STARTING_POS_Y = WORLD_DIM[1] * 2 // 10
SAUCER_POP_PERIOD_S = 30
SAUCER_EXPLOSION_DURATION_MS = 2000

### LASER ###
LASER_RECT_DIM = (2, 12)
LASER_H_BAR_DIM = (8, 2)
LASER_H_BAR_MOVE_SPEED = - 0.5
LASER_RECT_COLOR = (255, 255, 0)
LASER_SPEED_PIXEL_PER_SECOND = 100

### BARRICADES ###
BARRICADE_POSITIONS = [
    ((WORLD_DIM[0] // 18) + (WORLD_DIM[0] // 9 * 1), WORLD_DIM[1] * 8 // 10),
    ((WORLD_DIM[0] // 18) + (WORLD_DIM[0] // 9 * 3), WORLD_DIM[1] * 8 // 10),
    ((WORLD_DIM[0] // 18) + (WORLD_DIM[0] // 9 * 5), WORLD_DIM[1] * 8 // 10),
    ((WORLD_DIM[0] // 18) + (WORLD_DIM[0] // 9 * 7), WORLD_DIM[1] * 8 // 10)
]

LASER_BARRICADE_EXPLOSION_RADIUS = 8
MISSILE_BARRICADE_EXPLOSION_RADIUS = 4
BARRICADE_DESTRUCTION_PROBABILITY = 0.8

### SCORES ###
SCORE_DIGIT_COUNT = 5
SCORE_DIGIT_X_SPACE_PIXELS = 4
SCORE_POS = (WORLD_DIM[0] // 10, WORLD_DIM[1] // 10)
HIGH_SCORE_POS = (WORLD_DIM[0] // 10 * 5, WORLD_DIM[1] // 10)

### GAME_OVER ###
GAME_OVER_DURATION_S = 5
