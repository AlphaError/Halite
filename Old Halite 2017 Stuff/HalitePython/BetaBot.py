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
game = hlt.Game("Beta")
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
            hasUnowned = False
            isEnemy = False
            hasReadyFriendlyPlanet = False
            for planetNew in game_map.all_planets(): #method of finding the best planet
                if not planetNew.is_owned():
                    hasUnowned = True
                    if ship.calculate_distance_between(planetNew) < ship.calculate_distance_between(closest_planet):
                        closest_planet = planetNew
                if hasUnowned == False:
                    if (planetNew.owner.id == game_map.get_me().id) and (planetNew.is_full() == False):
                        hasReadyFriendlyPlanet = True
                        if ship.calculate_distance_between(planetNew) < ship.calculate_distance_between(closest_planet):
                            closest_planet = planetNew
                if (hasUnowned == False) and (hasReadyFriendlyPlanet == False):
                    isEnemy = True
                    if ship.calculate_distance_between(planetNew) < ship.calculate_distance_between(closest_planet):
                        closest_planet = planetNew
                if isEnemy == False:
                    for enemy in game_map.all_players():
                        if enemy.owner.id != game_map.get_me().id:
                            if ship.calculate_distance_between(enemy) < ship.calculate_distance_between(closest_planet):
                                if ship.calculate_distance_between(enemy) < ship.calculate_distance_between(bestEnemy):
                                    bestEnemy = enemy



                '''closest_planet = planet
                            hasUnowned = False
                            for planetNew in game_map.all_planets():
                                if not planetNew.is_owned():
                                    hasUnowned = True
                                    if ship.calculate_distance_between(planetNew) < ship.calculate_distance_between(closest_planet):
                                        closest_planet = planetNew
                    
                            hasReadyFriendlyPlanet = False
                            if hasUnowned == False:
                                for planetNewThree in game_map.all_planets():
                                    if (planetNewThree.owner.id == game_map.get_me().id) and (planetNewThree.is_full() == False):
                                        hasReadyFriendlyPlanet = True
                                        if ship.calculate_distance_between(planetNewThree) < ship.calculate_distance_between(closest_planet):
                                            closest_planet = planetNewThree

                            isEnemy = False
                            if (hasUnowned == False) and (hasReadyFriendlyPlanet == False):
                                isEnemy = True
                                for planetNewTwo in game_map.all_planets():
                                    if ship.calculate_distance_between(planetNewTwo) < ship.calculate_distance_between(closest_planet):
                                            closest_planet = planetNewTwo'''

            #if there is an unknown planet
            if hasUnowned == True:
                # If we can dock, let's (try to) dock. If two ships try to dock at once, neither will be able to.
                if ship.can_dock(closest_planet):
                    # We add the command by appending it to the command_queue
                    command_queue.append(ship.dock(closest_planet))
                else:
                    # If we can't dock, we move towards the closest empty point near this planet (by using closest_point_to)
                    # with constant speed. Don't worry about pathfinding for now, as the command will do it for you.
                    # We run this navigate command each turn until we arrive to get the latest move.
                    # Here we move at half our maximum speed to better control the ships
                    # In order to execute faster we also choose to ignore ship collision calculations during navigation.
                    # This will mean that you have a higher probability of crashing into ships, but it also means you will
                    # make move decisions much quicker. As your skill progresses and your moves turn more optimal you may
                    # wish to turn that option off.

                    if ship.calculate_distance_between(closest_planet) > (hlt.constants.DOCK_RADIUS * 1.9):
                        moveSpd = 1
                    else:
                        moveSpd = 1.5

                    navigate_command = ship.navigate(ship.closest_point_to(closest_planet), game_map, speed=hlt.constants.MAX_SPEED/moveSpd, ignore_ships=False)
                    # If the move is possible, add it to the command_queue (if there are too many obstacles on the way
                    # or we are trapped (or we reached our destination!), navigate_command will return null;
                    # don't fret though, we can run the command again the next turn)
                    if navigate_command:
                        command_queue.append(navigate_command)
                break
            #if there are no owned planets and there is an unfilled friendly planet
            elif (hasReadyFriendlyPlanet == True) and (closest_planet.is_full() == False):
                # If we can dock, let's (try to) dock. If two ships try to dock at once, neither will be able to.
                if ship.can_dock(closest_planet):
                    # We add the command by appending it to the command_queue
                    command_queue.append(ship.dock(closest_planet))
                else:
                    # If we can't dock, we move towards the closest empty point near this planet (by using closest_point_to)
                    # with constant speed. Don't worry about pathfinding for now, as the command will do it for you.
                    # We run this navigate command each turn until we arrive to get the latest move.
                    # Here we move at half our maximum speed to better control the ships
                    # In order to execute faster we also choose to ignore ship collision calculations during navigation.
                    # This will mean that you have a higher probability of crashing into ships, but it also means you will
                    # make move decisions much quicker. As your skill progresses and your moves turn more optimal you may
                    # wish to turn that option off.

                    if ship.calculate_distance_between(closest_planet) > (hlt.constants.DOCK_RADIUS * 1.9):
                        moveSpd = 1
                    else:
                        moveSpd = 1.5

                    navigate_command = ship.navigate(ship.closest_point_to(closest_planet), game_map, speed=hlt.constants.MAX_SPEED/moveSpd, ignore_ships=False)
                    # If the move is possible, add it to the command_queue (if there are too many obstacles on the way
                    # or we are trapped (or we reached our destination!), navigate_command will return null;
                    # don't fret though, we can run the command again the next turn)
                    if navigate_command:
                        command_queue.append(navigate_command)
                break
            #if the only best move is to attack
            elif isEnemy == True:
                if ship.calculate_distance_between(closest_planet) > (hlt.constants.DOCK_RADIUS * 1.9):
                    moveSpd = 1
                else:
                    moveSpd = 1.5

                navigate_command = ship.navigate(ship.closest_point_to(closest_planet), game_map, speed=hlt.constants.MAX_SPEED/moveSpd, ignore_ships=False)
                # If the move is possible, add it to the command_queue (if there are too many obstacles on the way
                # or we are trapped (or we reached our destination!), navigate_command will return null;
                # don't fret though, we can run the command again the next turn)
                if navigate_command:
                    command_queue.append(navigate_command)
                break
            #if everything goes to shit
            elif isEnemy == False:
                navigate_command = ship.navigate(ship.closest_point_to(bestEnemy), game_map, speed=hlt.constants.MAX_SPEED/1.7, ignore_ships=False)
                # If the move is possible, add it to the command_queue (if there are too many obstacles on the way
                # or we are trapped (or we reached our destination!), navigate_command will return null;
                # don't fret though, we can run the command again the next turn)
                if navigate_command:
                    command_queue.append(navigate_command)
                break
            else:
                continue
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