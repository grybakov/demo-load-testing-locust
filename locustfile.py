import uuid
import random

from locust import Locust, TaskSequence, HttpLocust, TaskSet, task, seq_task

from config import BASE_URL
from methods import parse_qa_url


# locust -f locustfile.py SearchUser TopicUser RandomUser


class SearchUserBehavior(TaskSet):

    @task(1)
    def fail_search(self):
        url_fail_search = BASE_URL + '{0}'.format('/search')
        fail_search_payload = {'q': uuid.uuid4().hex[:10]}
        self.client.request('GET', url_fail_search, params=fail_search_payload, verify=False)

    @task(10)
    def success_search(self):
        qa_items = ['js', 'python', 'java', 'api', 'ajax', 'soup', 'devops', 'load', 'php', 'domain', 'asp', 'core',
                    'learn', 'machine', 'docker', 'vagrant', 'django', 'flask']
        url_success_search = BASE_URL + '{0}'.format('/search')
        success_search_payload = {'q': qa_items[random.randint(1, len(qa_items)-1)]}
        success_search_response = self.client.request('GET', url_success_search, params=success_search_payload, verify=False)

        topic_link = parse_qa_url(success_search_response)
        self.client.request('GET', topic_link, verify=False)


class NewQuestions(TaskSet):

    @task(5)
    def view_new_questions(self):
        url_view_new = BASE_URL + '{0}'.format('/questions/latest')
        view_new_response = self.client.request('GET', url_view_new, verify=False)

        topic_link = parse_qa_url(view_new_response)
        self.client.request('GET', topic_link, verify=False)

    @task(1)
    def stop(self):
        self.interrupt()


class InterestingQuestions(TaskSet):

    @task(5)
    def view_interesting_questions(self):
        url_view_interesting = BASE_URL + '{0}'.format('/questions/interesting')
        view_interesting_response = self.client.request('GET', url_view_interesting, verify=False)

        topic_link = parse_qa_url(view_interesting_response)
        self.client.request('GET', topic_link, verify=False)


    @task(1)
    def stop(self):
        self.interrupt()


class QuestionsWithoutAnswers(TaskSet):

    @task(5)
    def view_without_answer(self):
        url_view_without = BASE_URL + '{0}'.format('/questions/without_answer')
        view_without_response = self.client.request('GET', url_view_without, verify=False)

        topic_link = parse_qa_url(view_without_response)
        self.client.request('GET', topic_link, verify=False)


    @task(1)
    def stop(self):
        self.interrupt()


class TopicUserBehavior(TaskSet):

    tasks = {NewQuestions: 10,
             InterestingQuestions: 15,
             QuestionsWithoutAnswers: 5}


class RandomUserBehavior(TaskSet):

    MAX_PAGE_COUNT = 106

    def _get_page(self):
        url_random_page = BASE_URL + '{0}'.format('/questions/interesting')
        random_page_response = self.client.request('GET', url_random_page,
                                                   params={'page': random.randint(1, 105)},
                                                   verify=False)
        return random_page_response

    @task(2)
    def get_random_page(self):
        self._get_page()


    @task(15)
    def get_random_page_and_random_post(self):
        random_page_response = self._get_page()
        if random_page_response.status_code == 200:
            topic_link = parse_qa_url(random_page_response)
            self.client.request('GET', topic_link, verify=False)
        else:
            pass


class SearchUser(HttpLocust):
    host = BASE_URL
    weight = 3
    task_set = SearchUserBehavior
    min_wait = 1 * 1000
    max_wait = 5 * 1000

class TopicUser(HttpLocust):
    host = BASE_URL
    weight = 3
    task_set = TopicUserBehavior
    min_wait = 0.5 * 1000
    max_wait = 5 * 1000

class RandomUser(HttpLocust):
    host = BASE_URL
    weight = 2
    task_set = RandomUserBehavior
    min_wait = 0.5 * 1000
    max_wait = 5 * 1000

