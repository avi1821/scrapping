
class Notification:

    def log(self, message):
        print(message)


    def error(self,  message):
        print(f"An error occurred: {message}")

notify = Notification()
