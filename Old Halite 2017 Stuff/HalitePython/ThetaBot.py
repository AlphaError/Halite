"""
Welcome to your first Halite-II bot!

This bot's name is Settler. It's purpose is simple (don't expect it to win complex games :) ):
1. Initialize game
2. If a ship is not docked and there are unowned planets
2.a. Try to Dock in the planet if close enough
2.b If not, go towards the planet

Note: Please do not place print statements here as they are used to communicate with the Halite engine. If you need
to log anything use the logging module.
"""
# Let's start by importing the Halite Starter Kit so we can interface with the Halite engine
import hlt
# Then let's import the logging module so we can print out information
import logging

# GAME START
# Here we define the bot's name as Settler and initialize the game, including communication with the Halite engine.
game = hlt.Game("Theta")
# Then we print our start message to the logs
logging.info("Starting my Settler bot!")

while True:
    # TURN START
    # Update the map for the new turn and get the latest version
    game_map = game.update_map()

    # Here we define the set of commands to be sent to the Halite engine at the end of the turn
    command_queue = []
    # For every ship that I control
    for ship in game_map.get_me().all_ships():
        # If the ship is docked
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            # Skip this ship
            continue

        # For each planet in the game (only non-destroyed planets are included)
        for planet in game_map.all_planets():

            closest_planet = planet
            #planetCount = 0
            for planetNew in game_map.all_planets():
                if not planetNew.is_owned():
                    #planetCount += 1
                    if ship.calculate_distance_between(planetNew) < ship.calculate_distance_between(closest_planet):
                        closest_planet = planetNew

            #navigate_command = ship.thrust(ship.closest_point_to(closest_planet), game_map, speed = hlt.constants.MAX_SPEED/1.8, max_corrections=210, ignore_ships = False, ignore_planets = True)
        
            if ship.can_dock(closest_planet): #if you are in docking range and it's not unowned
                deltaY = ship.y - closest_planet.y
                deltaX = ship.x - closest_planet.x
                navigate_command = ship.thrust(hlt.constants.MAX_SPEED/1.7, (math.atan2(deltaY, deltaX) + math.radians(90)))

                # If the move is possible, add it to the command_queue (if there are too many obstacles on the way
                # or we are trapped (or we reached our destination!), navigate_command will return null;
                # don't fret though, we can run the command again the next turn)
                if navigate_command:
                    command_queue.append(navigate_command)
                break
                        #atan2 delta y delta x
            else:
                # If we can't dock, we move towards the closest empty point near this planet (by using closest_point_to)
                # with constant speed. Don't worry about pathfinding for now, as the command will do it for you.
                # We run this navigate command each turn until we arrive to get the latest move.
                # Here we move at half our maximum speed to better control the ships
                # In order to execute faster we also choose to ignore ship collision calculations during navigation.
                # This will mean that you have a higher probability of crashing into ships, but it also means you will
                # make move decisions much quicker. As your skill progresses and your moves turn more optimal you may
                # wish to turn that option off.
                navigate_command = ship.navigate(ship.closest_point_to(closest_planet), game_map, speed=hlt.constants.MAX_SPEED/1.7, ignore_ships=False, ignore_planets=True)
                # If the move is possible, add it to the command_queue (if there are too many obstacles on the way
                # or we are trapped (or we reached our destination!), navigate_command will return null;
                # don't fret though, we can run the command again the next turn)
                if navigate_command:
                    command_queue.append(navigate_command)
            break

    # Send our set of commands to the Halite engine for this turn
    game.send_command_queue(command_queue)
    # TURN END
# GAME END
"""
def __init__ shipDock( Ship ship, Planet planet ):
    if ship.can_dock(planet):
        command_queue.append(ship.dock(planet))
    else:
        navigate_command = ship.navigate(ship.closest_point_to(planet), game_map, speed=hlt.constants.MAX_SPEED/2, ignore_ships=True)
        if navigate_command:
            command_queue.append(navigate_command)
    return None
"""

#running for online visualizer
#cd (file path)
#halite.exe "python MyBot.py" "python MyBot.py"
#halite.exe "java MyBot" "java MyBot" --> must build first though
#.\halite.exe -d '160 160' -t 'python3 MyBot.py' 'python3 MyBot.py'

