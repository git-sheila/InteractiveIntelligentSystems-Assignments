from collections import defaultdict

class Mood:
    def __init__(self, alpha=0.2):
        self.alpha = alpha  # Smoothing factor
        self.ema_buffer = defaultdict(float)  # Stores weighted values for emotions

    def update_emotion(self, current_emotion):
        # Update the EMA for the detected emotion
        for emotion in self.ema_buffer.keys():
            if emotion == current_emotion:
                self.ema_buffer[emotion] = self.alpha + (1 - self.alpha) * self.ema_buffer[emotion]
            else:
                self.ema_buffer[emotion] = (1 - self.alpha) * self.ema_buffer[emotion]

        # Handle new emotions not yet in the buffer
        if current_emotion not in self.ema_buffer:
            self.ema_buffer[current_emotion] = self.alpha

    def get_mood(self):
        # Return the emotion with the highest EMA value
        if self.ema_buffer:
            return max(self.ema_buffer, key=self.ema_buffer.get)
        return None  # No emotion detected yet