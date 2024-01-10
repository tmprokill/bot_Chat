# TELEGRAM BOT to use chat GPT

#### Description:
I embarked on developing this bot as my final project due to the ubiquitous use of Telegram in Ukraine, where it stands as the most widely used messenger. Additionally, Telegram bots have emerged as an integral part of the platform's ecosystem. My bot acts as an intermediary, leveraging the Telegram API and AIOGRAM library to facilitate seamless communication between users and OpenAI's GPT. Essentially, it creates a chat environment within the Telegram platform, enabling users to interact with the GPT model.

## Project Overview:
The project unfolds in distinct phases:
1. **Libraries and Routes Initialization:** Commencing with the importation of necessary libraries and the setup of routes for coroutines in Python, the groundwork was laid for seamless execution later in the Python file.

2. **File Object Class Creation:** A class for file objects was meticulously crafted to serve as the handler for voice files, streamlining the handling and manipulation of these specific file types within the bot's framework.

3. **Database and Bot Token Integration:** The pivotal connection between the bot's tokens and the database was established, ensuring smooth data flow and access between these essential components.

4. **Button Definition and Function Activation:** To enhance user interaction, I defined various buttons and their associated functions. Considering the project's diverse locales, these buttons were adapted to cater to specific user preferences.

5. **Routes and Handlers for API Functionality:** Delineated routes and their corresponding handlers were created to facilitate interactions with the API. These routes were integral in structuring the bot's operations in line with the API's functionalities.

6. **Implementation of Helper Functions:** Beyond the primary handler functions, a range of auxiliary functions was developed. For instance, the 'ask chat' function interacted with the database for user information and communicated with the chatGPT via API for testing purposes. Another key function, 'Transcript,' effectively converted voice messages into text, adding another layer of usability to the bot's features.

## Skills Acquired:
Reflecting on the learning curve and skill acquisition throughout this project, I honed various skills imparted by the CS50 course:
- **Fundamental Programming Skills:** The course provided a strong foundation in programming, laying the groundwork for this project's implementation.

- **Effective Library Utilization:** Proficiently importing and managing various libraries proved crucial in ensuring the bot's functionality.

- **Concurrent File Handling:** Simultaneously managing multiple files within the bot's framework demanded careful planning and execution.

- **Database Integration (sqlite3):** Incorporating sqlite3 databases into the bot's architecture enabled efficient data storage and retrieval.

- **Version Control via Commits:** Regular commits were instrumental in maintaining a track record of user data and bot functionality improvements.

- **Building an Internationalized Program:** Implementing multiple locales through JSON files was initially challenging but ultimately rewarding, broadening the bot's accessibility and appeal to diverse users.

- **Creation of a Virtual Environment (VENV):** Establishing a VENV was a significant milestone in my learning journey, showcasing newfound proficiency in managing environments for project development.

- **Transcription of Voice Messages:** A standout accomplishment was the implementation of a mechanism to transcribe voice messages. I devised a unique system to distribute these messages across five different files, effectively managing incoming data. When all files were occupied, the bot intelligently paused for 15 seconds, allowing the queue to clear before resuming operations.

## Conclusion:
In conclusion, I extend my heartfelt gratitude for the invaluable time and comprehensive guidance provided throughout this course. The opportunity to work on these engaging projects and delve deep into programming concepts has been immensely gratifying. Thank you for this enriching learning experience. Farewell!