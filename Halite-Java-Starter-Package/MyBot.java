//C:\Users\stewv\Documents\GitHub\Halite\Halite-Java-Starter-Package>runGame.bat
import java.util.ArrayList;
import java.util.Random;

/*
 * Strategies:
 * * tunnel through enemies
 * * collect reasources around players
 * * p view --> tunnel to high production places
 * * * early vs. mid vs. end/late game
 * * 255 strength 
 * * field id = 0
 */

public class MyBot {
    public static void main(String[] args) throws java.io.IOException {
        InitPackage iPackage = Networking.getInit();
        int myID = iPackage.myID;
        GameMap gameMap = iPackage.map;

        Networking.sendInit("Alpha Bot");

        Random rand = new Random();
        Direction moveDirection = null;
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
                                moveDirection = d;
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
                        
                        if(hasFriend == 1) {
                            //early game code for combination attack
                            for (Direction h : Direction.CARDINALS) { //for directions
                                if (gameMap.getSite(new Location(x, y), h).owner == myID) { //check and save friendly square
                                    Location friendly = gameMap.getLocation(new Location(x, y), h);
                                    for (Direction i : Direction.CARDINALS) { //for the directions around the friendly square
                                        if (gameMap.getSite(new Location(friendly), i).owner != myID && gameMap.getSite(new Location(friendly), i).strength <
                                        (gameMap.getSite(new Location(x, y)).strength + gameMap.getSite(new Location(friendly)).strength)) {
                                            //check if the an enemy square's strength is less than the frienly square + current moving square
                                            moves.add(new Move(new Location(x, y), h));
                                            moveDirection = h;
                                            movedPiece = true;
                                        }
                                    }
                                }
                            }
                        }
                        if(hasFriend == 2 || hasFriend == 3) {
                            //early game code for combination attack
                            
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
                            moveDirection = Direction.STILL;
                            movedPiece = true;
                        }

                        Direction bestF = Direction.STILL;
                        if(hasFriend >= 4) { //friendly code
                            // for each direction
                                // go in that direction until we see a square that isn't mine
                                // count the number of moves
                                // compare that to the best number of moves
                                // store the best direction
                            // move in the best direction
                            int bestNumberOfMoves = Integer.MAX_VALUE;
                            for (Direction f : Direction.CARDINALS) {
                                int currentNumberOfMoves = 1;
                                Location current = gameMap.getLocation(new Location(x, y), f);
                                while (currentNumberOfMoves < gameMap.width || currentNumberOfMoves < gameMap.height) {
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
                            }
                            
                            if(!movedPiece && gameMap.getSite(new Location(x, y)).strength < 
                            gameMap.getSite(new Location(x, y)).production * productionCount && gameMap.getSite(new Location(x, y)).production > 0) {
                               moves.add(new Move(new Location(x, y), Direction.STILL));
                               moveDirection = Direction.STILL;
                               movedPiece = true;
                            }
                            else if(!movedPiece && bestF != Direction.STILL) { //if should move but not still
                               moves.add(new Move(new Location(x, y), bestF));
                               moveDirection = bestF;
                               movedPiece = true;
                            }
                            else if(!movedPiece) { //random thing that changes every so often ^
                                moves.add(new Move(new Location(x, y), rand.nextBoolean() ? gameDirection1 : gameDirection2));
                                movedPiece = true;
                            }
                        }
                        
                        if(!movedPiece) { // fall back plan
                            moves.add(new Move(new Location(x, y), Direction.STILL));
                            moveDirection = Direction.STILL;
                            movedPiece = true;
                        }
                        
                        Location moving = gameMap.getLocation(new Location(x, y), moveDirection); //start of checking move code
                        for (Direction g : Direction.CARDINALS) {
                            if (gameMap.getSite(new Location(x, y), moveDirection).owner == 0) { //if moving location is field
                                if (gameMap.getSite(new Location(moving), g).owner != 0 && gameMap.getSite(new Location(moving), g).owner != myID) {
                                    moves.add(new Move(new Location(x, y), Direction.STILL)); //non aggression pact trial 1
                                }
                            }
                        }
                        int strengthLoss = 75; //allowance level of strength losted due to cap per particle (about 30%)
                        if (moveDirection != Direction.STILL && gameMap.getSite(new Location(moving)).owner == myID &&
                           (gameMap.getSite(new Location(moving)).strength + gameMap.getSite(new Location(x, y)).strength) > (255 + strengthLoss)) {
                            moves.add(new Move(new Location(x, y), Direction.STILL)); //stays still until 
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