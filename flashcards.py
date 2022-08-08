# Application for practicing flashcards
# Based on Python and database connected via SQLAlchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker

# Initialize the database and create new table via class

Base = declarative_base()


class Flashcard(Base):
	__tablename__ = 'flashcard'

	id = Column(Integer, primary_key=True)
	question = Column(String)
	answer = Column(String)
	box = Column(Integer, default=1)


# Main class managing the flashcards game


class GameSession:

	engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
	Base.metadata.create_all(engine)
	Session = sessionmaker(bind=engine)

	def __init__(self):
		self.counter = 0  # Updated every round to move up to another flashcard based on PK in the database

	@staticmethod
	def prompt_main_menu():  # Main menu for the game
		top_menu = input('\n1. Add flashcards\n2. Practice flashcards\n3. Exit\n')
		# Going over different possible answers
		while top_menu == '':
			game.prompt_main_menu()
		if top_menu not in ['1', '2', '3']:
			print(f'{top_menu} is not an option')
			game.prompt_main_menu()
		elif top_menu == '1':
			game.prompt_adding()
		elif top_menu == '2':
			game.prompt_practice()
		else:
			print('Bye!')
			exit()

	@staticmethod
	def prompt_adding(session = Session()):  # Method managing adding flashcards to the database
		add_menu = input('1. Add a new flashcard\n2. Exit\n')
		# Going over different possible answers
		while add_menu == '':
			game.prompt_adding()
		if add_menu not in ['1', '2']:
			print(f'{add_menu} is not an option')
			game.prompt_adding()
		if add_menu == '1':
			add_question = input('Question:').strip()
			while add_question == '':
				add_question = input('Question:').strip()
			add_answer = input('Answer:').strip()
			while add_answer == '':
				add_answer = input('Answer:').strip()
			flash_new = Flashcard(question=add_question, answer=add_answer)
			session.add(flash_new)
			session.commit()
			game.prompt_adding()
		elif add_menu == '2':
			print('Bye!')
			exit()

	def prompt_practice(self, session = Session()):  # Method managing practicing with flashcards
		flashcard_list = session.query(Flashcard).all()  # List of all the flashcards
		try:
			question = flashcard_list[self.counter].question.strip()
			answer = flashcard_list[self.counter].answer.strip()
			prompt_answer = input(f'Question: {question}:\npress "y" to see the answer:\npress "n" to skip:\npress "u" to update:\n')
			# Going over different possible answers
			while prompt_answer == '':
				game.prompt_practice()
			if prompt_answer == 'y':
				print(f'Answer: {answer}')
				game.prompt_correct_wrong()
			elif prompt_answer == 'n':
				self.counter += 1
				game.prompt_practice()
			elif prompt_answer == "u":
				game.edit()
			else:
				print(f'{prompt_answer} is not an option')
		except IndexError:  # Controls whether there is more flashcards available, if not error is prompted
			print('There is no flashcard to practice!\nBye!')
			exit()

	def edit(self, session = Session()):  # Method managing flashcards in the database
		flashcard_list = session.query(Flashcard).all()
		single_query = session.query(Flashcard)
		question = flashcard_list[self.counter].question.strip()
		answer = flashcard_list[self.counter].answer.strip()
		choice_del_edit = input('press "d" to delete the flashcard:\npress "e" to edit the flashcard:\n')
		# Going over different possible answers
		while choice_del_edit == '':
			game.prompt_practice()
		if choice_del_edit == 'd':
			single_query.filter(Flashcard.id == self.counter + 1).delete()  # +1 cause ID in SQL starts from 1 and counter from 0
			game.prompt_practice()
		elif choice_del_edit == 'e':
			print(f"current question: {question}")
			new_question = input("please write a new question: ")
			if new_question != '':
				card_filter = single_query.filter(Flashcard.question == question)
				card_filter.update({"question": new_question})
			print(f'current answer: {answer}')
			new_answer = input("please write a new answer: ")
			if new_answer != '':
				card_filter = single_query.filter(Flashcard.answer == answer)
				card_filter.update({"answer": new_answer})
			session.commit()
			self.counter += 1
			game.prompt_practice()
		else:
			print(f'{choice_del_edit} is not an option')

	def prompt_correct_wrong(self, session=Session()):
		query = session.query(Flashcard)
		card_filter = query.filter(Flashcard.id == self.counter + 1)  # +1 cause ID in SQL starts from 1 and counter from 0
		choice_yes_no = input('press "y" if your answer is correct:\npress "n" if your answer is wrong:\n')
		# Going over different possible answers
		while choice_yes_no == '':
			game.prompt_correct_wrong()
		if choice_yes_no == 'n':
			card_filter.update({'box': 1})
			session.commit()
			self.counter += 1
			game.prompt_practice()
		elif choice_yes_no == 'y':
			if query.filter(Flashcard.id == self.counter + 1, Flashcard.box == 3):
				card_filter.delete()  # Delete the card if it had reached the box number 3 (we know it well)
			else:
				card_filter.update({'box': 2})  # Move to next box two if answer is correct
				self.counter += 1
		else:
			print(f'{choice_yes_no} is not an option')
			game.prompt_correct_wrong()


if __name__ == '__main__':  # Initializing the game
	game = GameSession()
	game.prompt_main_menu()
