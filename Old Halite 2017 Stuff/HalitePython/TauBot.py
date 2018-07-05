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
game = hlt.Game("Tau")
# Then we print our start message to the logs
logging.info("Starting my Settler bot!")
moveCount = 0

while True:
    # TURN START
    # Update the map for the new turn and get the latest version
    game_map = game.update_map()

    command_queue = []

    fPlanetIndex = game_map.all_planets()
    inTotalShip = [0, 1 ,2]

    pos1 = hlt.entity.Position(0,0) #bot left
    pos2 = hlt.entity.Position(game_map.width, 0) #bot right
    pos3 = hlt.entity.Position(0, game_map.height) #top left
    pos4 = hlt.entity.Position(game_map.width, game_map.height) #top right
    escapeRoute = [pos1, pos2, pos3, pos4]

    countRand = 0

    myShips = game_map.get_me().all_ships()
    for current in range(0, len(myShips)):
        #ship = myShips[current]

        #for ship in game_map.get_me().all_ships():
        if myShips[current].docking_status != myShips[current].DockingStatus.UNDOCKED:
            continue

        for planet in game_map.all_planets():
            closest_planet = planet

            if (len(myShips) <= 3) and (moveCount <= 5): #code to diversift first 3 planets
                actualPlanet = game_map.all_planets()[0]
                shipNum = 0
                for x in inTotalShip: #for each ship
                    firstClosest = game_map.all_planets()[0]
                    for closerPlanet in fPlanetIndex:
                        if closerPlanet.is_owned() == False:
                            if myShips[x].calculate_distance_between(closerPlanet) < myShips[x].calculate_distance_between(firstClosest):
                                firstClosest = closerPlanet #calculates closest planet to said ship
                    if myShips[x].calculate_distance_between(firstClosest) < myShips[shipNum].calculate_distance_between(actualPlanet):
                        shipNum = x
                        actualPlanet = firstClosest

                if myShips[shipNum].can_dock(actualPlanet):
                    command_queue.append(myShips[shipNum].dock(actualPlanet))
                else:
                    angS = 5
                    if myShips[shipNum].calculate_distance_between(actualPlanet) > (hlt.constants.DOCK_RADIUS * 1.9):
                        moveSpd = 1
                        for closeShip in myShips:
                            if myShips[shipNum].calculate_distance_between(closeShip) < .35:
                                moveSpd = 1
                                angS = 9
                    else:
                        moveSpd = 1
                    navigate_command = myShips[shipNum].navigate(myShips[shipNum].closest_point_to(actualPlanet), game_map, speed=hlt.constants.MAX_SPEED/moveSpd, angular_step=angS, ignore_ships=False, ignore_planets=False)
                    if navigate_command:
                        command_queue.append(navigate_command)
                fPlanetIndex.remove(actualPlanet)
                inTotalShip.remove(shipNum)
                break
            elif (current == 1) and (moveCount < 30):   #initial attack stratagy
                attackPlan = game_map.all_planets()
                for plan in attackPlan:
                    if plan.is_owned() == False:
                        attackPlan.remove(plan)
                    elif plan.owner == game_map.get_me().id:
                        attackPlan.remove(plan)
                        #creates index with only enemy ships
                planetAttack = attackPlan[0]
                for attackYou in attackPlan:
                    if myShips[current].calculate_distance_between(attackYou) < myShips[current].calculate_distance_between(planetAttack):
                        planetAttack = attackYou
                enemyShip = planetAttack[0]
                navigate_command = myShips[current].navigate(myShips[current].closest_point_to(enemyShip), game_map, speed=hlt.constants.MAX_SPEED, angular_step=7, ignore_ships=False, ignore_planets=False)
                if navigate_command:
                    command_queue.append(navigate_command)
                break
            elif 2 > 1:
                enemyAttack = game_map._all_ships()[0] #initial declaration of a random enemy ***
                for v in game_map._all_ships():
                    if v.owner.id != game_map.get_me().id:
                        enemyAttack = v
                        break
                for f in game_map._all_ships():
                        if f.owner.id != game_map.get_me().id:
                            if closest_planet.calculate_distance_between(f) < closest_planet.calculate_distance_between(enemyAttack):
                                enemyAttack = f #now it is the enemy thats closest to the closest friendly planet
                countF = 0
                for friendlyCount in game_map.all_planets(): #counts friendly ships
                    if friendlyCount.is_owned():
                        if friendlyCount.owner.id == game_map.get_me().id:
                            countF += 1


                isWeakened = True #if the enemy has no owned planets
                for weakenedPlanet in game_map.all_planets():  #EXTRA ATTACK
                    if weakenedPlanet.is_owned():
                        if weakenedPlanet.owner.id != game_map.get_me().id:
                            isWeakened = False
                if isWeakened == True:
                    if moveCount > (10 * len(game_map.all_players())):
                        #enemy attack **
                        if myShips[current].calculate_distance_between(enemyAttack) > (hlt.constants.DOCK_RADIUS * 1.9):
                            moveSpd = 1
                        else:
                            moveSpd = 1.5
                        navigate_command = myShips[current].navigate(myShips[current].closest_point_to(enemyAttack), game_map, speed=hlt.constants.MAX_SPEED/moveSpd, angular_step=10, ignore_ships=False, ignore_planets=False)
                        if navigate_command:
                            command_queue.append(navigate_command)
                        break

                if (moveCount > 50) and (countF <= 1): #escape!
                    movePos = pos1
                    for x in range(0, len(escapeRoute)):
                        if myShips[current].calculate_distance_between(movePos) > myShips[current].calculate_distance_between(escapeRoute[x]):
                            movePos = escapeRoute[x]
                    #max movement speed
                    navigate_command = myShips[current].navigate(myShips[current].closest_point_to(movePos), game_map, speed=hlt.constants.MAX_SPEED, angular_step=10, ignore_ships=False, ignore_planets=False)
                    if navigate_command:
                        command_queue.append(navigate_command)
                    break


                for planetNew in game_map.all_planets(): #start of planet prioritizing code
                    if planetNew.is_owned():
                        if game_map.get_me().id == planetNew.owner.id:
                            if planetNew.is_full():
                                continue
                            if (moveCount > 190) and (myShips[current].calculate_distance_between(planetNew) > (game_map.width*.75)):
                                continue
                    if myShips[current].calculate_distance_between(planetNew) < myShips[current].calculate_distance_between(closest_planet):
                        closest_planet = planetNew #finally finds the closest planet


                if closest_planet.is_owned():
                    if game_map.get_me().id == closest_planet.owner.id:  #attack and defense
                        #enemyAttack **
                        if (moveCount >= 80) and (myShips[current].calculate_distance_between(closest_planet) < 1.2): #DEFENSE
                            #enemyAttack
                            if closest_planet.calculate_distance_between(enemyAttack) > 2.3: #spawn radius plus .3
                                if myShips[current].calculate_distance_between(enemyAttack) > (hlt.constants.DOCK_RADIUS*1.5):
                                    moveSpd = 1 #persuit
                                else:
                                    moveSpd = 1.3
                                navigate_command = myShips[current].navigate(myShips[current].closest_point_to(enemyAttack), game_map, speed=hlt.constants.MAX_SPEED/moveSpd, angular_step=10, ignore_ships=True, ignore_planets=False)
                                if navigate_command:
                                    command_queue.append(navigate_command)
                                break
                        elif (moveCount >= 25) and (myShips[current].calculate_distance_between(closest_planet) < .6): #DEFENSE
                            #enemyAttack
                            if closest_planet.calculate_distance_between(enemyAttack) > 2.3: #spawn radius plus .3
                                if myShips[current].calculate_distance_between(enemyAttack) > (hlt.constants.DOCK_RADIUS*1.5):
                                    moveSpd = 1 #persuit
                                else:
                                    moveSpd = 1.3
                                navigate_command = myShips[current].navigate(myShips[current].closest_point_to(enemyAttack), game_map, speed=hlt.constants.MAX_SPEED/moveSpd, angular_step=10, ignore_ships=True, ignore_planets=False)
                                if navigate_command:
                                    command_queue.append(navigate_command)
                                break
                        elif closest_planet.is_full(): #extra precausion
                            continue
                    elif (game_map.get_me().id != closest_planet.owner.id):
                        ship_list = closest_planet.all_docked_ships()

                        newShip = ship_list[0]
                        for x in ship_list:
                            if(myShips[current].calculate_distance_between(x) < myShips[current].calculate_distance_between(newShip)):
                                newShips = x

                        if myShips[current].calculate_distance_between(newShip) > (hlt.constants.DOCK_RADIUS * 2):
                            moveSpd = 1.1
                        else:
                            moveSpd = 1.5
                        navigate_command = myShips[current].navigate(myShips[current].closest_point_to(newShip), game_map, speed=hlt.constants.MAX_SPEED/moveSpd, angular_step=7, ignore_ships=False, ignore_planets=False)
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
                    navigate_command = myShips[current].navigate(myShips[current].closest_point_to(closest_planet), game_map, speed=hlt.constants.MAX_SPEED/moveSpd, angular_step=9, ignore_ships=False)
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