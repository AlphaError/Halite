//C:\Users\stewv\Documents\GitHub\Halite\Halite-Java-Starter-Package>runGame.bat
import java.util.ArrayList;
import java.util.Random;

public class MyBot {
    public static void main(String[] args) throws java.io.IOException {
        InitPackage iPackage = Networking.getInit();
        int myID = iPackage.myID;
        GameMap gameMap = iPackage.map;

        Networking.sendInit("Error Bot");

        Random rand = new Random();

        while(true) {
            ArrayList<Move> moves = new ArrayList<Move>();

            gameMap = Networking.getFrame();

            int frameCounter = 0;
            int productionCount = 5;
            Direction gameDirection1 = null;
            Direction gameDirection2 = null;
            for(int y = 0; y < gameMap.height; y++) {
                for(int x = 0; x < gameMap.width; x++) {
                    Site site = gameMap.getSite(new Location(x, y));
                    if(site.owner == myID) {
                        if(frameCounter <= 100) {
                            productionCount = 6;
                            gameDirection1 = Direction.NORTH;
                            gameDirection2 = Direction.EAST;
                        }
                        if(frameCounter > 100 && frameCounter <= 250) {
                            productionCount = 7;
                            gameDirection1 = Direction.SOUTH;
                            gameDirection2 = Direction.WEST;
                        }
                        if(frameCounter > 250) {
                            productionCount = 5;
                        }
                        
                        boolean movedPiece = false;
                        int hasFriend = 0;
                        int hasEnemy = 0;
                        for(Direction d : Direction.CARDINALS) {
                            if(gameMap.getSite(new Location(x, y), d).owner != myID &&
                            gameMap.getSite(new Location(x, y), d).strength < gameMap.getSite(new Location(x, y)).strength) {
                                moves.add(new Move(new Location(x, y), d));
                                movedPiece = true;
                                break;
                            }
                            
                            if(gameMap.getSite(new Location(x, y), d).owner == myID) { //adding counters to calculate the amount of friendly and enemy squares based on the current square
                                hasFriend += 1;
                            }
                            if(gameMap.getSite(new Location(x, y), d).owner != myID) {
                                hasEnemy += 1;
                            }
                        }
                        
                        Direction dNew = null; //enemy code
                        Direction dOld = null;
                        for(Direction e : Direction.CARDINALS) {
                            if(gameMap.getSite(new Location(x, y), e).owner != myID &&
                            gameMap.getSite(new Location(x, y), e).strength >= gameMap.getSite(new Location(x, y)).strength) {
                                e = dNew;
                                if(gameMap.getSite(new Location(x, y), dNew).owner != myID && 
                                gameMap.getSite(new Location(x, y), dNew).strength < gameMap.getSite(new Location(x, y), dOld).strength) {
                                    dOld = dNew;
                                } //finding the lowest enemy square in the vacinity
                            }
                        }
                        if(!movedPiece && gameMap.getSite(new Location(x, y), dOld).strength > gameMap.getSite(new Location(x, y)).strength) {
                            //if the weakest enemy square is still larger than us we stay still
                            moves.add(new Move(new Location(x, y), Direction.STILL));
                            movedPiece = true;
                        }
                        
                        
                        //Direction fNew = null;
                        int numToEnemy = 0;
                        int lastNumEnemy = 0;
                        int numEnemyCount = 0;
                        Direction bestF = null;
                        if(hasFriend >= 4) { //friendly code
                            for (Direction f : Direction.CARDINALS) {
                                ArrayList<Direction> dirs = new ArrayList<Direction>();
                                //Direction[] dirs = {};
                                dirs.add(f);
                                int arrayCount = 1;
                                numEnemyCount += 1;
                                Location newLoc = new Location(x, y);
                                for (int a = 0; arrayCount >= a; a++) {
                                    newLoc = gameMap.getSite(new Location(x, y), dirs[a]);
                                }
                                    while(gameMap.getSite(new Location(x, y), newLoc).owner == myID) {
                                       dirs.add(f); //adding 1 more move in that direction...?
                                       arrayCount += 1;
                                       numToEnemy += 1;
                                    }
                                if (numEnemyCount < 1) {
                                    lastNumEnemy = numToEnemy; //factoring in for the very first instance of the fNew
                                }
                                if (numEnemyCount >= 1 && numToEnemy < lastNumEnemy) {
                                    lastNumEnemy = numToEnemy; //making sure the variable will be at it's lowest for the next loop
                                    bestF = f; //setting the direction
                                }
                            }
                            if(!movedPiece && gameMap.getSite(new Location(x, y)).strength < gameMap.getSite(new Location(x, y)).production * productionCount) {
                               moves.add(new Move(new Location(x, y), Direction.STILL));
                               movedPiece = true;
                            }
                            if(!movedPiece) {
                               //moves.add(new Move(new Location(x, y), rand.nextBoolean() ? gameDirection1 : gameDirection2));
                               moves.add(new Move(new Location(x, y), bestF));
                               movedPiece = true;
                            }
                        }
                        
                        if(!movedPiece) { // fall back plan
                            moves.add(new Move(new Location(x, y), Direction.STILL));
                            movedPiece = true;
                        }
                        
                        
                        //if(movedPiece && gameMap.getSite(new Location(x, y)).strength >= 255) { //fallback #2 for it
                          //  moves.add(new Move(new Location(x, y), Direction.randomDirection()));
                        //}
                        
                        if (movedPiece) {
                            frameCounter += 1;
                        }
                    }
                }
            }
            Networking.sendFrame(moves);
        }
    }
}