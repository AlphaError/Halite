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
game = hlt.Game("Kapa")
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

        enemyAttack = game_map._all_ships()[0] #initial declaration of a random enemy ***
        for v in game_map._all_ships():
            if v.owner.id != game_map.get_me().id:
                enemyAttack = v
                break
        '''for randoShip in game_map._all_ships():
            if randoShip.owner != myShips[current].owner:
                enemyAttack = randoShip #now it is the enemy thats closest to the closest friendly planet
                break

        for enemyShip in game_map._all_ships():
            if enemyShip.owner.id != game_map.get_me().id:
                if myShips[current].calculate_distance_between(enemyShip) < myShips[current].calculate_distance_between(enemyAttack):
                    enemyAttack = enemyShip'''

        if myShips[current].calculate_distance_between(enemyAttack) > (hlt.constants.DOCK_RADIUS * 1.9):
            moveSpd = 1
        else:
            moveSpd = 1.5
        navigate_command = myShips[current].navigate(myShips[current].closest_point_to(enemyAttack), game_map, speed=hlt.constants.MAX_SPEED/moveSpd, angular_step=10, ignore_ships=False, ignore_planets=False)
        if navigate_command:
            command_queue.append(navigate_command)
        break

    # Send our set of commands to the Halite engine for this turn
    game.send_command_queue(command_queue)
    # TURN END
# GAME END
