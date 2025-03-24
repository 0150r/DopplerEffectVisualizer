import pygame
import time

# screen size
WIDTH = 1280
HEIGHT = 720

# extra space beyond the screen
PADDING = 50

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

SATELLITE_SPEED = 2
PULSE_SPEED = 200
PULSE_DELAY = 0.5

satellite_pos = [0, 100]
observer_pos = [WIDTH // 2, HEIGHT - 50]

pulses = []
last_pulse_time = time.time()
satellite_active = True # true=satellite can pulse
pulses_from_satellite = True # true=satellite is TXing, false=observer is TXing
paused = False

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("KH6WI Doppler Shift Simulation")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Main loop
running = True
while running:

    # Handle input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN: # pressing enter will toggle between observer RX and TX
                pulses_from_satellite = not pulses_from_satellite
                satellite_pos[0] = -PADDING
                satellite_active = True
                pulses.clear()
            elif event.key == pygame.K_SPACE: # pressing spacebar will pause the simulation
                paused = not paused
                if not paused: # when starting back up, clear all the pulses or it will look weird
                    pulses.clear()

    if paused:
        continue

    # clear screen
    screen.fill(BLACK)

    # move the satellite
    satellite_pos[0] += SATELLITE_SPEED
    if satellite_pos[0] > WIDTH + PADDING:  # off screen
        if pulses_from_satellite: # satellite is in TX mode
            if not pulses: # wait for all pulses to dissipate before starting a second pass
                satellite_pos[0] = -PADDING
                satellite_active = True
            else:
                satellite_active = False
        else:
            satellite_pos[0] = -PADDING
    
    # generate pulses every 0.5 seconds based on toggle
    current_time = time.time()
    if current_time - last_pulse_time >= PULSE_DELAY:
        last_pulse_time = current_time
        if pulses_from_satellite and satellite_active: # satellite is TXing
            pulses.append([satellite_pos[0], satellite_pos[1], current_time])
        elif not pulses_from_satellite: # observer is TXing
            pulses.append([observer_pos[0], observer_pos[1], current_time])

    # update and draw satellite pulses
    for pulse in pulses:
        time_elapsed = current_time - pulse[2]
        radius = PULSE_SPEED * time_elapsed
        if radius > WIDTH + PADDING:
            pulses.remove(pulse)
        else:
            pygame.draw.circle(screen, BLUE, (int(pulse[0]), int(pulse[1])), int(radius), 1)

    # draw satellite
    pygame.draw.circle(screen, RED, (satellite_pos[0], satellite_pos[1]), 10)

    # draw observer
    pygame.draw.circle(screen, WHITE, (observer_pos[0]+1, observer_pos[1]), 7) # head
    pygame.draw.line(screen, WHITE, (observer_pos[0], observer_pos[1]), (observer_pos[0], observer_pos[1]+20), 3) # body
    pygame.draw.line(screen, WHITE, (observer_pos[0]-8, observer_pos[1]+10), (observer_pos[0]+8, observer_pos[1]+10), 3) # arms
    pygame.draw.line(screen, WHITE, (observer_pos[0], observer_pos[1]+20), (observer_pos[0]-5, observer_pos[1]+30), 3) # left leg
    pygame.draw.line(screen, WHITE, (observer_pos[0], observer_pos[1]+20), (observer_pos[0]+5, observer_pos[1]+30), 3)# right leg

    # display who is transmitting
    if pulses_from_satellite:
        status_text = font.render("Receiving from Satellite", True, WHITE)
        screen.blit(status_text, (10, 10))
    else:
        status_text = font.render("Transmitting to Satellite", True, WHITE)
        screen.blit(status_text, (10, 10))

    status_text = font.render("NOT TO SCALE", True, WHITE)
    screen.blit(status_text, (10, HEIGHT - 30))

    # update display
    pygame.display.flip()

    # sleep until it's time to run the next frame and stay at 60fps
    clock.tick(60)

# quit pygame
pygame.quit()