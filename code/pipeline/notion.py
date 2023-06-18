import os
from dotenv import load_dotenv
from notion_client import Client
from pipeline import PipelineUsable
from datatypes import File

load_dotenv()

class Notion(PipelineUsable):
    # Notion integration constants
    NOTION_PAGE_ID = os.getenv('NOTION_PAGE')
    NOTION_DATABASE = os.getenv('NOTION_DATABASE')
    NOTION_TOKEN = os.getenv('NOTION_TOKEN')
    
    isOn = NOTION_TOKEN and NOTION_PAGE_ID
    client = None

    def setup(self):
        if self.isOn:
            self.logger('Initializing Notion client. Tokens were provided!')
            self.client = Client(auth=self.NOTION_TOKEN)
        else:
            self.logger('Notion integration is not setup. Skipping.')

    def append_highlight(self, info: tuple[str, str], file: File) -> None:
        if self.client is None:
            return

        self.logger('Adding highlight to notion.')

        title, text = info

        created_page_id = None

        if self.NOTION_DATABASE:
            pages = self.client.databases.query(
                database_id=self.NOTION_DATABASE,
                filter={
                    'property': 'Name',
                    'rich_text': {
                        'equals': title
                    }
                }
            )

            if len(list(pages['results'])) == 0:
                new_page = {
                    "Name": { "title": [{ "text": { "content": title } }] },
                }

                self.client.pages.create(
                    parent={"database_id": self.NOTION_DATABASE},
                    properties=new_page
                )

                pages = self.client.databases.query(
                    database_id=self.NOTION_DATABASE,
                    filter={
                        'property': 'Name',
                        'rich_text': {
                            'equals': title
                        }
                    }
                )

                created_page_id = pages['results'][0]['id']
            else:
                created_page_id = pages['results'][0]['id']

        page_id = self.NOTION_PAGE_ID if self.NOTION_DATABASE is None else created_page_id

        self.client.blocks.children.append(str(page_id), children=[
            {
                'type': 'paragraph',
                'paragraph': {
                    'rich_text': [{
                        'type': 'text',
                        'text': {
                            'content': 'saved at: {}'.format(file.format_created_at())
                        },
                        'annotations': {
                            'italic': True,
                            'color': 'gray'
                        }
                    }]
                }
            },
            {
                'type': 'paragraph',
                'paragraph': {
                    'rich_text': [{
                        'type': 'text',
                        'text': {
                            'content': text.strip()
                        }
                    }]
                }
            },
            {
                'type': 'paragraph',
                'paragraph': {
                    'rich_text': [{
                        'type': 'text',
                        'text': {
                            'content': ''
                        }
                    }]
                }
            },
            {
                'type': 'paragraph',
                'paragraph': {
                    'rich_text': [{
                        'type': 'text',
                        'text': {
                            'content': ''
                        }
                    }]
                }
            },
        ])

