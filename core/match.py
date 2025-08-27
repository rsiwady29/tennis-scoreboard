"""
Core match logic for tennis scoring system.
Implements standard tennis rules for points, games, sets, and matches.
"""

from typing import Dict, Any, List, Tuple
from .observer import Subject


class Match(Subject):
    """
    Represents a tennis match with full scoring logic.
    
    Tennis scoring rules:
    - Points: 0 → 15 → 30 → 40 → Advantage → Game
    - Games: First to 6 with 2-game margin, otherwise continue until margin reached
    - Sets: Best of 3 (configurable)
    - Deuce: At 40-40, must win by 2 points
    - Advantage: Win next point after deuce to win game
    - Tiebreak: At 6-6 games, first to 7 points (with 2-point margin) wins set
    """
    
    def __init__(self, best_of_sets: int = 3):
        super().__init__()
        self.best_of_sets = best_of_sets
        self.reset()
    
    def reset(self) -> None:
        """Reset match to initial state."""
        self.sets = [0, 0]  # [home, away]
        self.games = [0, 0]  # [home, away]
        self.points = [0, 0]  # [home, away]
        self.server = 0  # 0 = home, 1 = away
        self.match_complete = False
        self.winner = None
        
        # Tiebreak state
        self.in_tiebreak = False
        self.tiebreak_points = [0, 0]  # [home, away]
        
        self._notify_state_change()
    
    def home_scores_point(self) -> None:
        """Home player scores a point."""
        if not self.match_complete:
            self._score_point(0)
    
    def away_scores_point(self) -> None:
        """Away player scores a point."""
        if not self.match_complete:
            self._score_point(1)
    
    def swap_server(self) -> None:
        """Swap the current server."""
        self.server = 1 - self.server
        self._notify_state_change()
    
    def _score_point(self, player: int) -> None:
        """Internal method to score a point for the specified player."""
        if self.match_complete:
            return
        
        if self.in_tiebreak:
            # Scoring in tiebreak
            self.tiebreak_points[player] += 1
            
            # Check if tiebreak is won
            if self._is_tiebreak_won(player):
                self._win_set(player)
                self.games = [0, 0]  # Reset games
                self.points = [0, 0]  # Reset points
                self.in_tiebreak = False
                self.tiebreak_points = [0, 0]
        else:
            # Regular game scoring
            self.points[player] += 1
            
            # Check if game is won
            if self._is_game_won(player):
                self._win_game(player)
                self.points = [0, 0]  # Reset points
                
                # Check if set is won
                if self._is_set_won(player):
                    self._win_set(player)
                    self.games = [0, 0]  # Reset games
                
                # Check if tiebreak should start
                elif self._should_start_tiebreak():
                    self.in_tiebreak = True
                    self.points = [0, 0]  # Reset regular points
                    self.tiebreak_points = [0, 0]  # Initialize tiebreak points
        
        # Check if match is won
        if self._is_match_won(player):
            self._win_match(player)
        
        self._notify_state_change()
    
    def _is_game_won(self, player: int) -> bool:
        """Check if the specified player has won the current game."""
        opponent = 1 - player
        
        # Standard game win (40+ and 2+ point lead)
        if (self.points[player] >= 4 and 
            self.points[player] - self.points[opponent] >= 2):
            return True
        
        # Deuce/Advantage logic
        if self.points[player] >= 4 and self.points[opponent] >= 4:
            # At deuce (40-40), need 2 point lead
            if self.points[player] - self.points[opponent] >= 2:
                return True
        
        return False
    
    def _is_set_won(self, player: int) -> bool:
        """Check if the specified player has won the current set."""
        opponent = 1 - player
        
        # Standard set win (6+ games with 2+ game lead)
        if (self.games[player] >= 6 and 
            self.games[player] - self.games[opponent] >= 2):
            return True
        
        # Set win via tiebreak
        if self.in_tiebreak and self._is_tiebreak_won(player):
            return True
        
        return False
    
    def _should_start_tiebreak(self) -> bool:
        """Check if a tiebreak should start (both players at 6 games)."""
        return self.games[0] == 6 and self.games[1] == 6
    
    def _is_tiebreak_won(self, player: int) -> bool:
        """Check if the specified player has won the tiebreak."""
        opponent = 1 - player
        
        # First to 7 points wins tiebreak
        if self.tiebreak_points[player] >= 7:
            # Must win by 2 points if opponent has 5+ points
            if self.tiebreak_points[opponent] <= 5:
                return True
            elif self.tiebreak_points[player] - self.tiebreak_points[opponent] >= 2:
                return True
        
        return False
    
    def _is_match_won(self, player: int) -> bool:
        """Check if the specified player has won the match."""
        sets_needed = (self.best_of_sets // 2) + 1
        return self.sets[player] >= sets_needed
    
    def _win_game(self, player: int) -> None:
        """Record a game win for the specified player."""
        self.games[player] += 1
        # Server changes after each game
        self.swap_server()
    
    def _win_set(self, player: int) -> None:
        """Record a set win for the specified player."""
        self.sets[player] += 1
        # Server changes after each set
        self.swap_server()
    
    def _win_match(self, player: int) -> None:
        """Record a match win for the specified player."""
        self.match_complete = True
        self.winner = player
    
    def _notify_state_change(self) -> None:
        """Notify all observers of state change."""
        self.notify(self.get_state())
    
    def get_state(self) -> Dict[str, Any]:
        """Get current match state as a dictionary."""
        return {
            'sets': self.sets.copy(),
            'games': self.games.copy(),
            'points': self.points.copy(),
            'server': self.server,
            'match_complete': self.match_complete,
            'winner': self.winner,
            'server_name': 'Home' if self.server == 0 else 'Away',
            'in_tiebreak': self.in_tiebreak,
            'tiebreak_points': self.tiebreak_points.copy()
        }
    
    def get_score_display(self) -> Dict[str, str]:
        """Get formatted score strings for display."""
        if self.in_tiebreak:
            points_display = f"Tiebreak: {self.tiebreak_points[0]} - {self.tiebreak_points[1]}"
        else:
            points_display = self._format_points()
        
        return {
            'sets': f"{self.sets[0]} - {self.sets[1]}",
            'games': f"{self.games[0]} - {self.games[1]}",
            'points': points_display,
            'server': 'Home' if self.server == 0 else 'Away'
        }
    
    def _format_points(self) -> str:
        """Format points according to tennis scoring."""
        point_names = ['0', '15', '30', '40']
        
        home_points = self.points[0]
        away_points = self.points[1]
        
        # Handle deuce and advantage
        if home_points >= 3 and away_points >= 3:
            if home_points == away_points:
                return '40 - 40'  # Deuce
            elif home_points > away_points:
                return 'Advantage - 40'
            else:
                return '40 - Advantage'
        
        # Standard scoring
        home_display = point_names[min(home_points, 3)]
        away_display = point_names[min(away_points, 3)]
        return f"{home_display} - {away_display}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert match state to dictionary for persistence."""
        return {
            'best_of_sets': self.best_of_sets,
            'sets': self.sets,
            'games': self.games,
            'points': self.points,
            'server': self.server,
            'match_complete': self.match_complete,
            'winner': self.winner,
            'in_tiebreak': self.in_tiebreak,
            'tiebreak_points': self.tiebreak_points
        }
    
    def from_dict(self, data: Dict[str, Any]) -> None:
        """Load match state from dictionary."""
        self.best_of_sets = data.get('best_of_sets', 3)
        self.sets = data.get('sets', [0, 0])
        self.games = data.get('games', [0, 0])
        self.points = data.get('points', [0, 0])
        self.server = data.get('server', 0)
        self.match_complete = data.get('match_complete', False)
        self.winner = data.get('winner', None)
        self.in_tiebreak = data.get('in_tiebreak', False)
        self.tiebreak_points = data.get('tiebreak_points', [0, 0])
        self._notify_state_change()
