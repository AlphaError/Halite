//C:\Users\stewv\Documents\GitHub\Halite\Halite-Java-Starter-Package>runGame.bat
import java.util.ArrayList;
import java.util.Random;

public class MyBot {
    public static void main(String[] args) throws java.io.IOException {
        InitPackage iPackage = Networking.getInit();
        int myID = iPackage.myID;
        GameMap gameMap = iPackage.map;

        Networking.sendInit("Alpha Bot");

        Random rand = new Random();
        int frameCounter = 0;
        int oldFrame = 0;
        int productionCount = 5;
        while(true) {
            ArrayList<Move> moves = new ArrayList<Move>();
            gameMap = Networking.getFrame();
            for(int y = 0; y < gameMap.height; y++) {
                for(int x = 0; x < gameMap.width; x++) {
                    Site site = gameMap.getSite(new Location(x, y));
                    if(site.owner == myID) { //general frame analysis for 
                            Direction gameDirection1 = Direction.NORTH;
                            Direction gameDirection2 = Direction.EAST;
                        if(frameCounter <= 80 ) {
                            productionCount = 6;
                        }
                        if(frameCounter > 80 && frameCounter <= 250) {
                            productionCount = 7;
                        }
                        if(frameCounter > 250) {
                            productionCount = 5;
                        }
                        if ((oldFrame +  80) <= frameCounter) { //suppesedly changes the random direction in which the particles go every '80'
                            if (gameDirection1 == Direction.NORTH) { //north --> east, east --> south, south --> west, west --> north
                                gameDirection1 = Direction.EAST;
                            }
                            if (gameDirection1 == Direction.EAST) { //north --> east, east --> south, south --> west, west --> north
                                gameDirection1 = Direction.SOUTH;
                            }
                            if (gameDirection1 == Direction.SOUTH) { //north --> east, east --> south, south --> west, west --> north
                                gameDirection1 = Direction.WEST;
                            }
                            if (gameDirection1 == Direction.WEST) { //north --> east, east --> south, south --> west, west --> north
                                gameDirection1 = Direction.NORTH;
                            }
                            
                            if (gameDirection2 == Direction.NORTH) { //north --> east, east --> south, south --> west, west --> north
                                gameDirection2 = Direction.EAST;
                            }
                            if (gameDirection2 == Direction.EAST) { //north --> east, east --> south, south --> west, west --> north
                                gameDirection2 = Direction.SOUTH;
                            }
                            if (gameDirection2 == Direction.SOUTH) { //north --> east, east --> south, south --> west, west --> north
                                gameDirection2 = Direction.WEST;
                            }
                            if (gameDirection2 == Direction.WEST) { //north --> east, east --> south, south --> west, west --> north
                                gameDirection2 = Direction.NORTH;
                            }
                            oldFrame = frameCounter;
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
                        Direction bestF = Direction.STILL;
                        if(hasFriend >= 4) { //friendly code
                            // for each direction
                                // go in that direction until we see a square that isn't mine
                                // count the number of moves
                                // compare that to the best number of moves
                                // store the best direction
                            // move in the best direction
                            int bestNumberOfMoves = 1000;
                      
                            for (Direction f : Direction.CARDINALS) {
                                int currentNumberOfMoves = 1;
                                Location current = gameMap.getLocation(new Location(x, y), f);
                                while (current.x != x && current.y != y) {
                                    if (gameMap.getSite(current).owner != myID) {
                                        if (currentNumberOfMoves < bestNumberOfMoves) {
                                            bestNumberOfMoves = currentNumberOfMoves;
                                            bestF = f;
                                        }
                                        break;
                                    }
                                    current = gameMap.getLocation(current, f);
                                    currentNumberOfMoves++;
                                }
                                
                                
                                /*ArrayList<Direction> dirs = new ArrayList<Direction>();
                                dirs.add(f);
                                int dirsSize = dirs.size();
                                for (int a = 0; dirsSize >= a; a++) {
                                    if(gameMap.getSite(new Location(x, y), dirs.get(a)).owner == myID) {
                                       dirs.add(f); //adding 1 more move in that direction then rechecking for an enemy
                                    }
                                }
                                numToEnemy = dirs.size(); //for clarity
                                if (numEnemyCount < 1) {
                                    lastNumEnemy = numToEnemy; //factoring in for the very first instance of the fNew
                                }
                                if (numEnemyCount >= 1 && numToEnemy < lastNumEnemy) {
                                    lastNumEnemy = numToEnemy; //making sure the variable will be at it's lowest for the next loop
                                    bestF = f; //setting the direction
                                }*/
                            }
                            
                            if(!movedPiece && gameMap.getSite(new Location(x, y)).strength <
                            gameMap.getSite(new Location(x, y)).production * productionCount) {
                               moves.add(new Move(new Location(x, y), Direction.STILL));
                               movedPiece = true;
                            }
                            else if(!movedPiece) {
                               //moves.add(new Move(new Location(x, y), rand.nextBoolean() ? gameDirection1 : gameDirection2));
                               moves.add(new Move(new Location(x, y), bestF));
                               movedPiece = true;
                            }
                        }
                        
                        if(!movedPiece) { // fall back plan
                            moves.add(new Move(new Location(x, y), Direction.STILL));
                            movedPiece = true;
                        }
                        
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