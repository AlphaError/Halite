import java.util.ArrayList;

import hlt.*;
import hlt.Constants;
import hlt.DockMove;
import hlt.GameMap;
import hlt.Move;
import hlt.Navigation;
import hlt.Networking;
import hlt.Planet;
import hlt.Ship;
import hlt.ThrustMove;

/**
 * 
 */

/**
 * @author Alpha Error - Stewart H.
 * -For 2 Sigma's Halite II competition
 */
public class AlphaBot {

	/**
	 * @param args
	 */
	public static void main(final String[] args) {
        final Networking networking = new Networking();
        final GameMap gameMap = networking.initialize("Tamagocchi");

        final ArrayList<Move> moveList = new ArrayList<>(); //list of moves
        for (;;) {
            moveList.clear(); //clears list
            gameMap.updateMap(Networking.readLineIntoMetadata());

            for (final Ship ship : gameMap.getMyPlayer().getShips().values()) { //for each ship value
                if (ship.getDockingStatus() == Ship.DockingStatus.Docked || ship.getDockingStatus()  == Ship.DockingStatus.Docking) { //if docked or docking
                	for (final Planet planet : gameMap.getAllPlanets().values()) {
                		if(planet.isOwned() == true) {
                			if(ship.canDock(planet)) { //always doc at a planet
                                moveList.add(new DockMove(ship, planet));
                                break;
                            }
                            final ThrustMove newThrustMove = Navigation.navigateShipToDock(gameMap, ship, planet, Constants.MAX_SPEED/2);
                            if (newThrustMove != null) {
                                moveList.add(newThrustMove);
                            }
                            break;
                		}
                		//continues onto another planet
                    }
                	//continues onto another
                }
                else if(ship.getDockingStatus() == Ship.DockingStatus.Undocked || ship.getDockingStatus() == Ship.DockingStatus.Undocking) { //if undocked
                	for (final Planet planet : gameMap.getAllPlanets().values()) {
                		if(planet.isOwned() == true) { //if friendly planet
                			if(planet.getCurrentProduction() <= (5/6) ) { //if production is sufficient --> produces 5 ships per 6 turns
                				moveList.add(new DockMove(ship, planet));
                                break;
                			}
                			//continue onto next planet
                		}
                		else if(planet.isOwned() == false) { //if its an unknown planet
                			if((planet.getHealth() / 4) < ship.getHealth()) {
                				moveList.add(new DockMove(ship, planet));
                                break;
                			}//if it will take <=4 ships to take the planet
//                			else if(gameMap.nearbyEntitiesByDistance(ship.getId())<0> )
                			
                			else { //if the non-me planet hasn't been taken
                				moveList.add(new DockMove(ship, planet));
                                break;
                			}
                		}
                	}
                }
                //nearby_entities_by_distance
                System.out.println(ship.toString());
            }
            Networking.sendMoves(moveList);
            
        }
//        public void attackTarget(Ship ship, Ship target) { //takes in a ship and a target, checks the values of each and the attack cooldown
//        	if(ship.getWeaponCooldown() == 0) {
//        		
//        	}
//        }
    }

	/* Strategy:
	 * Passive Protocol:
	 * * Docked Ships--> If production is below a certain level and there is no enemy within a close radius stay put and produce.
	 * * UnDocked Ships --> search for nearest low-level planet that can be captured with all available undocked friendly ships and capture it
	 * * Docking/Undocking --> continue with normal capturing  protocol
	 * Attack Protocol: ( assuming there is an enemy within close range)
	 * * Intercept enemy at 1 move distance and group up around planets at 1 move distances to defend
	 * 
	 */
}
