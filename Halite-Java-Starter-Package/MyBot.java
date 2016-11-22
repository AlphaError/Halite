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

            for(int y = 0; y < gameMap.height; y++) {
                for(int x = 0; x < gameMap.width; x++) {
                    Site site = gameMap.getSite(new Location(x, y));
                    if(site.owner == myID) {

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
                        
                        Direction dNew = null;
                        Direction dOld = null;
                        for(Direction e : Direction.CARDINALS) {
                            if(gameMap.getSite(new Location(x, y), e).owner != myID &&
                            gameMap.getSite(new Location(x, y), e).strength >= gameMap.getSite(new Location(x, y)).strength) {
                                e = dNew;
                                if(gameMap.getSite(new Location(x, y), dNew).strength < gameMap.getSite(new Location(x, y), dOld).strength) {
                                    dOld = dNew;
                                } //finding the lowest enemy square in the vacinity
                            }
                        }
                        if(!movedPiece && gameMap.getSite(new Location(x, y), dOld).strength > gameMap.getSite(new Location(x, y)).strength) {
                            //if the weakest enemy square is still larger than us we stay still
                            moves.add(new Move(new Location(x, y), Direction.STILL));
                            movedPiece = true;
                        }
                        
                        if(hasFriend >= 4) {
                           Direction eNew = null;
                           Direction eOld = null;
                           for(Direction e : Direction.CARDINALS) {
                               if(gameMap.getSite(new Location(x, y), e).owner == myID &&
                                  gameMap.getSite(new Location(x, y), e).strength < gameMap.getSite(new Location(x, y)).strength) {
                                  e = dNew;
                                 if(gameMap.getSite(new Location(x, y), eNew).strength < gameMap.getSite(new Location(x, y), eOld).strength) {
                                    eOld = eNew;
                                 } //finding the lowest friendly square in the vacinity
                               }
                           }
                           if(!movedPiece && gameMap.getSite(new Location(x, y), eOld).strength < gameMap.getSite(new Location(x, y)).strength && 
                           (gameMap.getSite(new Location(x, y), eOld).strength + gameMap.getSite(new Location(x, y)).strength) < 255) {
                               //if the weakest enemy square is still larger than us we move to it assuming them combined isn't max (using 255 as the maxium stregnth scaling)
                               moves.add(new Move(new Location(x, y), eOld));
                               movedPiece = true;
                           }
                           if(!movedPiece && (gameMap.getSite(new Location(x, y), eOld).strength + gameMap.getSite(new Location(x, y)).strength) >=255) {
                               moves.add(new Move(new Location(x, y), Direction.WEST));
                               //making sure that the piece moves in one continuous direction to start attacking pieces
                            }
                        }
                        
                        if(!movedPiece) { // fall back plan
                            moves.add(new Move(new Location(x, y), Direction.STILL));
                        }
                        
                        
                        //if(movedPiece && gameMap.getSite(new Location(x, y)).strength >= 255) { //fallback #2 for it
                          //  moves.add(new Move(new Location(x, y), Direction.randomDirection()));
                        //}
                    }
                }
            }
            Networking.sendFrame(moves);
        }
    }
}