from bs4 import BeautifulSoup
import requests
import threading
from os import path, remove

class SdamGIA:
    def __init__(self):
        self._BASE_DOMAIN = 'sdamgia.ru'
        self._SUBJECT_BASE_URL = {
            'math': f'https://math-ege.{self._BASE_DOMAIN}', 'mathb': f'https://mathb-ege.{self._BASE_DOMAIN}',
            'phys': f'https://phys-ege.{self._BASE_DOMAIN}',
            'inf': f'https://inf-ege.{self._BASE_DOMAIN}',
            'rus': f'https://rus-ege.{self._BASE_DOMAIN}',
            'bio': f'https://bio-ege.{self._BASE_DOMAIN}',
            'en': f'https://en-ege.{self._BASE_DOMAIN}',
            'chem': f'https://chem-ege.{self._BASE_DOMAIN}',
            'geo': f'https://geo-ege.{self._BASE_DOMAIN}',
            'soc': f'https://soc-ege.{self._BASE_DOMAIN}',
            'de': f'https://de-ege.{self._BASE_DOMAIN}',
            'fr': f'https://fr-ege.{self._BASE_DOMAIN}',
            'lit': f'https://lit-ege.{self._BASE_DOMAIN}',
            'sp': f'https://sp-ege.{self._BASE_DOMAIN}',
            'hist': f'https://hist-ege.{self._BASE_DOMAIN}',
        }
        self.tesseract_src = 'tesseract'

    def get_problem_by_id(self, subject, id, img=None, path_to_img=None, path_to_html='', grabzit_auth=None):
        """
        Получение информации о задаче по ее идентификатору

        :param subject: Наименование предмета
        :type subject: str

        :param id: Идентификатор задачи
        :type subject: str

        :param img: Принимает одно из двух значений: pyppeteer или grabzit;
                    В результате будет использована одна из библиотек для генерации изображения с задачей.
                    Если не передавать этот аргумент, изображение генерироваться не будет
        :type img: str

        :param path_to_img: Путь до изображения, куда сохранить сохранить задание.
        :type path_to_img: str

        :param path_to_html: Можно указать директорию, куда будут сохраняться временные html-файлы заданий при использовании pyppeteer
        :type path_to_html: str

        :param grabzit_auth: При использовании GrabzIT укажите данные для аутентификации: {"AppKey":"...", "AppSecret":"..."}
        :type grabzit_auth: dict
        """

        doujin_page = requests.get(
            f'{self._SUBJECT_BASE_URL[subject]}/problem?id={id}')
        soup = BeautifulSoup(doujin_page.content, 'html.parser')

        probBlock = soup.find('div', {'class': 'prob_maindiv'})
        if probBlock is None:
            return None
        print(probBlock)
        for i in probBlock.find_all('img'):
            if not 'sdamgia.ru' in i['src']:
                i['src'] = self._SUBJECT_BASE_URL[subject] + i['src']


        URL = f'{self._SUBJECT_BASE_URL[subject]}/problem?id={id}'
        TOPIC_ID = ' '.join(probBlock.find(
            'span', {'class': 'prob_nums'}).text.split()[1:][:-2])
        ID = id

        CONDITION, SOLUTION, ANSWER, ANALOGS = {}, {}, '', []

        try:
            CONDITION = {'text': probBlock.find_all('div', {'class': 'pbody'})[0].text,
                         'images': [i['src'] for i in probBlock.find_all('div', {'class': 'pbody'})[0].find_all('img')]
                         }
        except IndexError:
            pass

        try:
            SOLUTION = {'text': probBlock.find_all('div', {'class': 'pbody'})[1].text,
                        'images': [i['src'] for i in probBlock.find_all('div', {'class': 'pbody'})[1].find_all('img')]
                        }
        except IndexError:
            pass
        except AttributeError:
            pass

        try:
            ANSWER = probBlock.find(
                'div', {'class': 'answer'}).text.replace('Ответ: ', '')
        except IndexError:
            pass
        except AttributeError:
            pass

        try:
            ANALOGS = [i.text for i in probBlock.find(
                'div', {'class': 'minor'}).find_all('a')]
            if 'Все' in ANALOGS:
                ANALOGS.remove('Все')
        except IndexError:
            pass
        except AttributeError:
            pass


        if not img is None:

            for i in probBlock.find_all('div', {'class': 'minor'}):
                i.decompose()
            probBlock.find_all('div')[-1].decompose()


            if img == 'pyppeteer':
                import asyncio
                from pyppeteer import launch
                open(f'{path_to_html}{id}.html', 'w').write(str(probBlock))
                async def main():
                    browser = await launch()
                    page = await browser.newPage()
                    await page.goto('file:' + path.abspath(f'{path_to_html}{id}.html'))
                    await page.screenshot({'path': path_to_img, 'fullPage': 'true'})
                    await browser.close()
                asyncio.get_event_loop().run_until_complete(main())
                remove(path.abspath(f'{path_to_html}{id}.html'))
            elif img == 'grabzit':
                from GrabzIt import GrabzItClient, GrabzItImageOptions
                grabzIt = GrabzItClient.GrabzItClient(grabzit_auth['AppKey'], grabzit_auth['AppSecret'])
                options = GrabzItImageOptions.GrabzItImageOptions()
                options.browserWidth = 800
                options.browserHeight = -1
                grabzIt.HTMLToImage(str(probBlock), options=options)
                grabzIt.SaveTo(path_to_img)

        return {'id': ID, 'topic': TOPIC_ID, 'condition': CONDITION, 'solution': SOLUTION, 'answer': ANSWER,
                'analogs': ANALOGS, 'url': URL}

    def search(self, subject, request, page=1):
        """
        Поиск задач по запросу

        :param subject: Наименование предмета
        :type subject: str

        :param request: Запрос
        :type request: str

        :param page: Номер страницы поиска
        :type page: int
        """
        doujin_page = requests.get(
            f'{self._SUBJECT_BASE_URL[subject]}/search?search={request}&page={str(page)}')
        soup = BeautifulSoup(doujin_page.content, 'html.parser')
        return [i.text.split()[-1] for i in soup.find_all('span', {'class': 'prob_nums'})]

    def get_test_by_id(self, subject, testid):
        """
        Получение списка задач, включенных в тест

        :param subject: Наименование предмета
        :type subject: str

        :param testid: Идентификатор теста
        :type testid: str
        """
        doujin_page = requests.get(
            f'{self._SUBJECT_BASE_URL[subject]}/test?id={testid}')
        soup = BeautifulSoup(doujin_page.content, 'html.parser')
        return [i.text.split()[-1] for i in soup.find_all('span', {'class': 'prob_nums'})]

    def get_category_by_id(self, subject, categoryid, page=1):
        """
        Получение списка задач, включенных в категорию

        :param subject: Наименование предмета
        :type subject: str

        :param categoryid: Идентификатор категории
        :type categoryid: str

        :param page: Номер страницы поиска
        :type page: int
        """

        doujin_page = requests.get(
            f'{self._SUBJECT_BASE_URL[subject]}/test?&filter=all&theme={categoryid}&page={page}')
        soup = BeautifulSoup(doujin_page.content, 'html.parser')
        return [i.text.split()[-1] for i in soup.find_all('span', {'class': 'prob_nums'})]

    def get_catalog(self, subject):
        """
        Получение каталога заданий для определенного предмета

        :param subject: Наименование предмета
        :type subject: str
        """

        doujin_page = requests.get(
            f'{self._SUBJECT_BASE_URL[subject]}/prob_catalog')
        soup = BeautifulSoup(doujin_page.content, 'html.parser')
        catalog = []
        CATALOG = []

        for i in soup.find_all('div', {'class': 'cat_category'}):
            try:
                i['data-id']
            except:
                catalog.append(i)

        for topic in catalog[1:]:
            TOPIC_NAME = topic.find(
                'b', {'class': 'cat_name'}).text.split('. ')[1]
            TOPIC_ID = topic.find(
                'b', {'class': 'cat_name'}).text.split('. ')[0]
            if TOPIC_ID[0] == ' ':
                TOPIC_ID = TOPIC_ID[2:]
            if TOPIC_ID.find('Задания ') == 0:
                TOPIC_ID = TOPIC_ID.replace('Задания ', '')

            CATALOG.append(
                dict(
                    topic_id=TOPIC_ID,
                    topic_name=TOPIC_NAME,
                    categories=[
                        dict(
                            category_id=i['data-id'],
                            category_name=i.find(
                                'a', {'class': 'cat_name'}).text
                        )
                        for i in
                        topic.find('div', {'class': 'cat_children'}).find_all('div', {'class': 'cat_category'})]
                )
            )

        return CATALOG

    def generate_test(self, subject, problems=None):
        """
        Генерирует тест по заданным параметрам

        :param subject: Наименование предмета
        :type subject: str

        :param problems: Список заданий
        По умолчанию генерируется тест, включающий по одной задаче из каждого задания предмета.
        Так же можно вручную указать одинаковое количество задач для каждого из заданий: {'full': <кол-во задач>}
        Указать определенные задания с определенным количеством задач для каждого: {<номер задания>: <кол-во задач>, ... }
        :type problems: dict
        """

        if problems is None:
            problems = {'full': 1}

        if 'full' in problems:
            dif = {f'prob{i}': problems['full'] for i in range(
                1, len(self.get_catalog(subject)) + 1)}
        else:
            dif = {f'prob{i}': problems[i] for i in problems}

        return requests.get(f'{self._SUBJECT_BASE_URL[subject]}/test?a=generate', dif,
                            allow_redirects=False).headers['location'].split('id=')[1].split('&nt')[0]

    def generate_pdf(self, subject, testid, solution='', nums='',
                     answers='', key='', crit='',
                     instruction='', col='', pdf=True):

        def a(a):
            if a == False:
                return ''
            return a

        return self._SUBJECT_BASE_URL[subject] + requests.get(f'{self._SUBJECT_BASE_URL[subject]}/test?'
                                                              f'id={testid}&print=true&pdf={pdf}&sol={a(solution)}&num={a(nums)}&ans={a(answers)}'
                                                              f'&key={a(key)}&crit={a(crit)}&pre={a(instruction)}&dcol={a(col)}',
                                                              allow_redirects=False).headers['location']


    def generate_answ_pdf(self, subject, testid, solution='', nums='',
                     answers=True, key='', crit='',
                     instruction='', col='', pdf=True):

        def a(a):
            if a == False:
                return ''
            return a

        return self._SUBJECT_BASE_URL[subject] + requests.get(f'{self._SUBJECT_BASE_URL[subject]}/test?'
                                                              f'id={testid}&print=true&pdf={pdf}&sol={a(solution)}&num={a(nums)}&ans={answers}'
                                                              f'&key={a(key)}&crit={a(crit)}&pre={a(instruction)}&dcol={a(col)}',
                                                              allow_redirects=False).headers['location']

    def generate_pdf_by_one(self, subject, problem_id):

        def a(a):
            if a == False:
                return ''
            return a

        return f'{self._SUBJECT_BASE_URL[subject]}/problem?'f'id={problem_id}&print=true&&svg=0&num=true'


sdg = SdamGIA()

if __name__ == '__main__':
    sdamgia = SdamGIA()
    test = sdamgia.get_problem_by_id('math', '505452')
    print(test)
