import os
from dotenv import load_dotenv
from notion_client import Client
from pipeline import PipelineUsable
from datatypes import File

load_dotenv()

class Notion(PipelineUsable):
    # Notion integration constants
    NOTION_PAGE_ID = os.getenv('NOTION_PAGE')
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

        self.client.blocks.children.append(str(self.NOTION_PAGE_ID), children=[
            {
                'type': 'heading_2',
                'heading_2': {
                    'rich_text': [{
                        'type': 'text',
                        'text': {
                            'content': title
                        }
                    }]
                },
            },
            {
                'type': 'paragraph',
                'paragraph': {
                    'rich_text': [{
                        'type': 'text',
                        'text': {
                            'content': text
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
                            'content': 'created at: {}'.format(file.format_created_at())
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
            }
        ])

