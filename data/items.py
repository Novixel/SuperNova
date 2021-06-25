# Classes for portfolio
from dataclasses import dataclass, field, InitVar

# Needs to be fine tunned
# But it works very well

@dataclass
class AccountItem:
    """Class for keeping track of an account."""
    _main: InitVar[dict] = None
    id: str = field(default_factory= str )
    currency: str = field(default_factory= str )
    balance: float = field(default_factory= float)
    hold: float = field(default_factory= float)
    available: float = field(default_factory= float)
    profile_id: str = field(default_factory= str )
    trading_enabled: bool = field(default_factory= bool)

    def __post_init__(self,_main):
        self.id: str = _main["id"]
        self.currency: str = _main["currency"]
        self.balance: float = _main["balance"]
        self.hold: float = _main["hold"]
        self.available: float = float(_main["available"])
        self.profile_id: str = _main["profile_id"]
        self.trading_enabled: bool = _main["trading_enabled"]

@dataclass
class ProductItem:
    """Class for keeping track of a product."""
    _main: InitVar[dict] = None
    id: str = field(default_factory= str )
    base_currency: str = field(default_factory= str )
    quote_currency: str = field(default_factory= str )
    base_min_size: float = field(default_factory= float)
    base_max_size: float = field(default_factory= float)
    quote_increment: float = field(default_factory= float)
    base_increment: float = field(default_factory= float)
    display_name: str = field(default_factory= str )
    min_market_funds: float = field(default_factory= float)
    max_market_funds: float = field(default_factory= float)
    margin_enabled: bool = field(default_factory= bool)
    post_only: bool = field(default_factory= bool)
    limit_only: bool = field(default_factory= bool)
    cancel_only: bool = field(default_factory= bool)
    trading_disabled: bool = field(default_factory= bool)
    status: str = field(default_factory= str )
    status_message: str = field(default_factory= str )

    def __post_init__(self,_main):
        self.id: str = _main["id"]
        self.base_currency: str = _main["base_currency"]
        self.quote_currency: str = _main["quote_currency"]
        self.base_min_size: float = _main["base_min_size"]
        self.base_max_size: float = _main["base_max_size"]
        self.quote_increment: float = _main["quote_increment"]
        self.base_increment: float = _main["base_increment"]
        self.display_name: str = _main["display_name"]
        self.min_market_funds: float = _main["min_market_funds"]
        self.max_market_funds: float = _main["max_market_funds"]
        self.margin_enabled: bool = _main["margin_enabled"]
        self.post_only: bool = _main["post_only"]
        self.limit_only: bool = _main["limit_only"]
        self.cancel_only: bool = _main["cancel_only"]
        self.trading_disabled: bool = _main["trading_disabled"]
        self.status: str = _main["status"]
        self.status_message: str = _main["status_message"]