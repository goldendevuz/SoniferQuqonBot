import uuid
from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator


class BaseModel(models.Model):
    """
    Abstract base model with UUID PK, timestamps, and common utilities.
    All models should inherit from this class.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
        help_text="Timestamp when the object was created",
        null=True,
        blank=True,
    )
    modified = models.DateTimeField(
        auto_now=True,
        verbose_name="Modified At",
        help_text="Timestamp when the object was last modified",
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
        ordering = ["-created"]  # Default ordering: newest first
        get_latest_by = "created"


class ButtonMedia(BaseModel):
    class KeyboardButton(models.TextChoices):
        ALL_CATEGORIES = "ALL_CATEGORIES", "ALL_CATEGORIES"
        MY_PROFILE = "MY_PROFILE", "MY_PROFILE"
        FAQ = "FAQ", "FAQ"
        HELP = "HELP", "HELP"
        CART = "CART", "CART"
        ADMIN_MENU = "MENU", "MENU"

    media_id = models.CharField(max_length=255)

    button = models.CharField(
        max_length=50,
        choices=KeyboardButton.choices,
        unique=True
    )

    class Meta:
        db_table = "buttons_media"

    def __str__(self):
        return f"{self.button} → {self.media_id}"
    

class Buy(BaseModel):
    buyer = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="buys"
    )

    quantity = models.IntegerField(
        validators=[MinValueValidator(1)]
    )

    total_price = models.DecimalField(
        max_digits=36,
        decimal_places=12,
        validators=[MinValueValidator(Decimal("0.000000000001"))]
    )

    buy_datetime = models.DateTimeField(
        auto_now_add=True
    )

    is_refunded = models.BooleanField(
        default=False
    )

    coupon = models.ForeignKey(
        "Coupon",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="buys"
    )

    class Meta:
        db_table = "buys"

    def __str__(self):
        return f"Buy #{self.id} - {self.quantity} pcs, total {self.total_price}"
    

class BuyItem(BaseModel):
    buy = models.ForeignKey(
        "Buy",
        on_delete=models.CASCADE,
        related_name="buy_items"
    )

    item = models.ForeignKey(
        "Item",
        on_delete=models.CASCADE,
        related_name="item_buy_items"
    )

    class Meta:
        db_table = "buyItem"

    def __str__(self):
        return f"Buy {self.buy_id} → Item {self.item_id}"


class Cart(BaseModel):
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="carts"
    )

    class Meta:
        db_table = "carts"

    def __str__(self):
        return f"Cart #{self.id} (User {self.user_id})"


class CartItem(BaseModel):
    cart = models.ForeignKey(
        "Cart",
        on_delete=models.CASCADE,
        related_name="items"
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="cart_items"
    )
    subcategory = models.ForeignKey(
        "Subcategory",
        on_delete=models.CASCADE,
        related_name="cart_items"
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        db_table = "cart_items"

    def __str__(self):
        return f"Cart {self.cart_id} - Category {self.category_id} - Subcategory {self.subcategory_id} ({self.quantity})"


class Category(BaseModel):
    name = models.CharField(
        max_length=255,
        unique=True,
        db_index=True
    )
    media_id = models.CharField(max_length=255)

    class Meta:
        db_table = "categories"

    def __str__(self):
        return self.name


class Coupon(BaseModel):
    class CouponType(models.TextChoices):
        PERCENT = "PERCENT", "Percent"
        FIXED = "FIXED", "Fixed"
    
    code = models.CharField(
        max_length=12,
        unique=True,
        db_index=True
    )
    type = models.CharField(
        max_length=10,
        choices=CouponType.choices
    )
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    create_datetime = models.DateTimeField()
    expire_datetime = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    usage_limit = models.IntegerField(default=1)
    usage_count = models.IntegerField(default=0)

    class Meta:
        db_table = "coupons"

    def __str__(self):
        return f"{self.code} ({self.type}) - {self.value}"


class Deposit(BaseModel):    
    class Cryptocurrency(models.TextChoices):
        BNB = "BNB"
        BTC = "BTC"
        LTC = "LTC"
        ETH = "ETH"
        SOL = "SOL"
    
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="deposits"
    )
    network = models.CharField(
        max_length=20,
        choices=Cryptocurrency.choices
    )
    amount = models.BigIntegerField(
        validators=[MinValueValidator(1)]
    )
    deposit_datetime = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "deposits"

    def __str__(self):
        return f"Deposit #{self.id} - {self.user_id} - {self.amount} {self.network}"


class Item(BaseModel):
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="items"
    )
    subcategory = models.ForeignKey(
        "Subcategory",
        on_delete=models.CASCADE,
        related_name="items"
    )
    private_data = models.TextField()
    price = models.DecimalField(
        max_digits=36,
        decimal_places=12,
        validators=[MinValueValidator(Decimal("0.000000000001"))]
    )
    is_sold = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    description = models.TextField()

    class Meta:
        db_table = "items"

    def __str__(self):
        return f"Item #{self.id} - {self.description[:30]}"


class Payment(BaseModel):
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="payments"
    )
    processing_payment_id = models.IntegerField()
    message_id = models.IntegerField()
    is_paid = models.BooleanField(default=False)
    expire_datetime = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "payments"

    def __str__(self):
        return f"Payment #{self.id} - User {self.user_id} - Paid: {self.is_paid}"

    
class Subcategory(BaseModel):
    name = models.CharField(
        max_length=255,
        db_index=True
    )
    media_id = models.CharField(max_length=255)

    class Meta:
        db_table = "subcategories"

    def __str__(self):
        return self.name


class User(BaseModel):
    class Language(models.TextChoices):
        EN = "EN", "English"
        RU = "RU", "Russian"
        UZ = "UZ", "Uzbek"
        FR = "fr"
        DE = "de"
        IT = "it"
        ZH = "zh"
        AR = "ar"
        ES = "es"
        JA = "ja"

    telegram_username = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        db_index=True
    )
    telegram_id = models.BigIntegerField(
        unique=True,
        db_index=True
    )

    top_up_amount = models.DecimalField(
        max_digits=36,
        decimal_places=12,
        default=Decimal("0"),
        validators=[MinValueValidator(Decimal("0"))]
    )
    consume_records = models.DecimalField(
        max_digits=36,
        decimal_places=12,
        default=Decimal("0"),
        validators=[MinValueValidator(Decimal("0"))]
    )

    registered_at = models.DateTimeField(auto_now_add=True)
    can_receive_messages = models.BooleanField(default=True)
    language = models.CharField(
        max_length=2,
        choices=Language.choices,
        default=Language.EN
    )

    class Meta:
        db_table = "users"

    def __str__(self):
        return f"{self.telegram_username or self.telegram_id}"