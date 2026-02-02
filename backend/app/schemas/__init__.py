"""
Pydantic schemas
"""
from .article import (
    ArticleBase,
    ArticleCreate,
    ArticleUpdate,
    Article,
    ArticleList,
)
from .subscriber import (
    SubscriberBase,
    SubscriberCreate,
    SubscriberUpdate,
    Subscriber,
    SubscriberList,
    SubscriberImport,
)
from .newsletter import (
    NewsletterBase,
    NewsletterCreate,
    NewsletterUpdate,
    Newsletter,
    NewsletterList,
    NewsletterWithArticles,
    NewsletterSendRequest,
)
from .template import (
    TemplateBase,
    TemplateCreate,
    TemplateUpdate,
    Template,
    TemplateList,
)

__all__ = [
    # Article
    "ArticleBase",
    "ArticleCreate",
    "ArticleUpdate",
    "Article",
    "ArticleList",
    # Subscriber
    "SubscriberBase",
    "SubscriberCreate",
    "SubscriberUpdate",
    "Subscriber",
    "SubscriberList",
    "SubscriberImport",
    # Newsletter
    "NewsletterBase",
    "NewsletterCreate",
    "NewsletterUpdate",
    "Newsletter",
    "NewsletterList",
    "NewsletterWithArticles",
    "NewsletterSendRequest",
    # Template
    "TemplateBase",
    "TemplateCreate",
    "TemplateUpdate",
    "Template",
    "TemplateList",
]
