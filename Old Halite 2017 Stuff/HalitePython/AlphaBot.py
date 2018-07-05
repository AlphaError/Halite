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
game = hlt.Game("Alpha")
# Then we print our start message to the logs
logging.info("Starting my Settler bot!")
moveCount = 0
while True:
    # TURN START
    # Update the map for the new turn and get the latest version
    game_map = game.update_map()

    command_queue = []

    myShips = game_map.get_me().all_ships()
    for current in range(0, len(myShips)):
        #ship = myShips[current]

    #for ship in game_map.get_me().all_ships():
        if myShips[current].docking_status != myShips[current].DockingStatus.UNDOCKED:
            continue

        for planet in game_map.all_planets():
            closest_planet = planet                

            isWeakened = True #if the enemy has no owned planets
            for weakenedPlanet in game_map.all_planets():  #EXTRA ATTACK
                if weakenedPlanet.is_owned():
                    if weakenedPlanet.owner.id != game_map.get_me().id:
                        isWeakened = False
            if isWeakened == True:
                if moveCount > 10:
                    enemyAttack = game_map._all_ships()[0]
                    for y in game_map._all_ships():
                        if y.owner.id != game_map.get_me().id:
                            enemyAttack = y
                    for z in game_map._all_ships():
                        if z.owner.id != game_map.get_me().id:
                            if myShips[current].calculate_distance_between(z) < myShips[current].calculate_distance_between(enemyAttack):
                                enemyAttack = z
                    if myShips[current].calculate_distance_between(enemyAttack) > (hlt.constants.DOCK_RADIUS * 1.9):
                        moveSpd = 1
                    else:
                        moveSpd = 1.5
                    navigate_command = myShips[current].navigate(myShips[current].closest_point_to(enemyAttack), game_map, speed=hlt.constants.MAX_SPEED/moveSpd, angular_step=5, ignore_ships=False, ignore_planets=False)
                    if navigate_command:
                        command_queue.append(navigate_command)
                    break


            unownedCount = 0
            for planetidk in game_map.all_planets():
                #if planetidk.is_owned() and (planetidk.owner.id == game_map.get_me().id):
                    #planetMyCount++
                if planetidk.is_owned() == False:
                    unownedCount += 1

            for planetNew in game_map.all_planets():
                if planetNew.is_owned():
                    if len(myShips) < 5:
                        #if I don't have that many ships prioritize getting more planets
                         #avoids wierd stalemates
                        continue
                    #if unownedCount >= (len(game_map.all_planets()) / (len(game_map.all_players())+1)):
                        #if the number of unowned planets is greater than all planets / number of players
                        #continue #calculate multiple ship distance
                    if game_map.get_me().id == planetNew.owner.id:
                        if planetNew.is_full():
                                continue
                        if myShips[current].calculate_distance_between(planetNew) > hlt.constants.DOCK_RADIUS * 4:
                            #don't move to a friendly planet that is more than x ship-lengths away (prioritize colonization first)
                            continue
                if myShips[current].calculate_distance_between(planetNew) < myShips[current].calculate_distance_between(closest_planet):
                    closest_planet = planetNew


            if closest_planet.is_owned():
                if game_map.get_me().id == closest_planet.owner.id:
                    if closest_planet.is_full(): #extra precausion
                        continue
                elif (game_map.get_me().id != closest_planet.owner.id):
                    ship_list = closest_planet.all_docked_ships()

                    newShip = ship_list[0]
                    '''for x in xrange(0, len(ship_list)):
                        if(ship.calculate_distance_between(newShip) > ship.calculate_distance_between(ship_list[x])):
                            newShip = ship_list[x]'''
                    for x in ship_list:
                        if(myShips[current].calculate_distance_between(x) < myShips[current].calculate_distance_between(newShip)):
                            newShips = x

                    #navigate_command = ship.navigate(ship.closest_point_to(newShip), game_map, speed=hlt.constants.MAX_SPEED/moveSpd, angular_step=5, ignore_ships=True, ignore_planets=False)
                    
                    #ship_list = closest_planet.all_docked_ships()
                    if myShips[current].calculate_distance_between(newShip) > (hlt.constants.DOCK_RADIUS * 1.9):
                        moveSpd = 1
                    else:
                        moveSpd = 1.6
                    navigate_command = myShips[current].navigate(myShips[current].closest_point_to(newShip), game_map, speed=hlt.constants.MAX_SPEED/moveSpd, angular_step=5, ignore_ships=False, ignore_planets=False)
                    if navigate_command:
                        command_queue.append(navigate_command)
                    break

            if myShips[current].can_dock(closest_planet):
                command_queue.append(myShips[current].dock(closest_planet))
            else:
                if myShips[current].calculate_distance_between(closest_planet) > (hlt.constants.DOCK_RADIUS * 2):
                    moveSpd = 1
                    if (moveCount < 7) and (len(myShips) <= 3):
                        moveSpd = 1.4
                else:
                    moveSpd = 1.7

                navigate_command = myShips[current].navigate(myShips[current].closest_point_to(closest_planet), game_map, speed=hlt.constants.MAX_SPEED/moveSpd, angular_step=5, ignore_ships=False)
                if navigate_command:
                    command_queue.append(navigate_command)
            break
    # Send our set of commands to the Halite engine for this turn
    game.send_command_queue(command_queue)
    moveCount += 1
    # TURN END
# GAME END

#running for online visualizer
#cd (file path)
#halite.exe "python MyBot.py" "python MyBot.py"
#halite.exe "java MyBot" "java MyBot" --> must build first though
#.\halite.exe -d '160 160' -t 'python3 MyBot.py' 'python3 MyBot.py'