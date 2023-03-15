from django.test import TestCase
#from user.models import User
from user.models import User
from stock.models import Company, Product, Stock, CompanyWarehouse, Threshold
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


# Create your tests here.
class CompanyModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user = User.objects.create(username='testuser', password='testpass')
        Company.objects.create(name='Test Company', address='Test Address', created_by=test_user)
    
    def test_company_name(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')
        
    def test_company_address(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('address').verbose_name
        self.assertEquals(field_label, 'address')
        
    def test_company_created_by(self):
        company = Company.objects.get(id=1)
        field_label = company._meta.get_field('created_by').verbose_name
        self.assertEquals(field_label, 'created by')
        
    def test_company_str_method(self):
        company = Company.objects.get(id=1)
        self.assertEquals(str(company), 'Test Company')


class ProductModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user = User.objects.create(username='testuser', password='testpass')
        test_company = Company.objects.create(name='Test Company', address='Test Address', created_by=test_user)
        Product.objects.create(name='Test Product', description='Test Description', company=test_company, unit_price=10.0, profit_margin=0.5, quantity_in_stock=10, minimum_quantity=5, quantity_ordered=0, reorder_quantity=10, rotation=0, on_clearance=False, on_sale=False, image='test_product.jpg')
    
    def test_product_name(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')
        
    def test_product_description(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')
        
    def test_product_company(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('company').verbose_name
        self.assertEquals(field_label, 'company')
        
    def test_product_str_method(self):
        product = Product.objects.get(id=1)
        self.assertEquals(str(product), 'Test Product')


class StockModelTestCase(TestCase):
    def create_user(self, username="testuser", password="testpass"):
        user = User.objects.create_user(
            username=username, password=password
        )
        return user
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.user2 = User.objects.create_user(
            username='testuser2', password='testpass'
        )
        self.company = Company.objects.create(name='Test Company', created_by = self.user2)
        self.warehouse = CompanyWarehouse.objects.create(
            name='Test Warehouse', company=self.company
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            quantity_in_stock=0,
            profit_margin = 1,
            company = self.company
        )
        self.stock = Stock.objects.create(
            product=self.product,
            quantity=0,
            warehouse=self.warehouse,
        )
    """ def test_user_can_restock(self):
        self.client.force_login(self.user2)
        response = self.client.put(
            reverse('stock-restock', args=[self.stock.pk]),
            data={'quantity': 10},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) """
        
    """ def test_stock_quantity_cannot_be_negative(self):
        self.stock.quantity = -5
        self.stock.save() # assurez-vous que le stock a été enregistré
        self.assertEqual(Stock.objects.count(), 1) # assurez-vous que le stock est bien enregistré
        with self.assertRaises(ValidationError):
            self.stock.full_clean() 
    
    def test_stock_in_transit_cannot_be_greater_than_quantity(self):
        self.stock.quantity = 5
        self.stock.in_transit = 10
        with self.assertRaises(ValidationError):
            self.stock.full_clean()
    
    def test_stock_status_is_updated_correctly_on_delivery(self):
        self.stock.on_delivery = True
        self.stock.save()
        self.assertEqual(self.stock.in_transit, True)
        self.assertEqual(self.stock.on_delivery, True)
    
    def test_stock_status_is_updated_correctly_on_reorder(self):
        self.stock.on_reorder = True
        self.stock.save()
        self.assertEqual(self.stock.on_reorder, True)
    
    def test_stock_status_is_updated_correctly_on_return(self):
        self.stock.on_return = True
        self.stock.save()
        self.assertEqual(self.stock.on_return, True)"""
    
    """ def test_stock_status_is_updated_correctly_when_stock_is_replenished(self):
        self.stock.quantity = 0
        self.stock.save()
        self.product.quantity_in_stock = 25
        self.product.save()
        self.assertEqual(self.stock.quantity, 25)
        self.assertEqual(self.stock.quantity, self.product.quantity_in_stock)
        self.assertEqual(self.stock.in_transit, False)
        self.assertEqual(self.stock.on_delivery, False)
        self.assertEqual(self.stock.on_reorder, False)
        self.assertEqual(self.stock.on_return, False) """ 
        
    """ def test_stock_status_is_updated_correctly_when_stock_is_replenished(self):
        self.stock.quantity = 0
        self.stock.save()
        self.product.quantity_in_stock = 25
        self.product.save()
        self.assertEqual(self.stock.quantity, 0)
        self.assertEqual(self.stock.in_transit, False)
        self.assertEqual(self.stock.on_delivery, False)
        self.assertEqual(self.stock.on_reorder, False)
        self.assertEqual(self.stock.on_return, False)
        
        # Réapprovisionner le stock
        response = self.client.put(reverse('stock-restock', kwargs={'pk': self.stock.id}), {'quantity': 25})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Vérifier que le stock et le produit ont été mis à jour correctement
        self.stock.refresh_from_db()
        self.product.refresh_from_db()
        self.assertEqual(self.stock.quantity, 25)
        self.assertEqual(self.product.quantity_in_stock, 25)
        self.assertEqual(self.stock.in_transit, False)
        self.assertEqual(self.stock.on_delivery, False)
        self.assertEqual(self.stock.on_reorder, False)
        self.assertEqual(self.stock.on_return, False) """


class ThresholdTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Test Company", address="Test Address")
        self.threshold = Threshold.objects.create(name="Test Threshold", value=10, company=self.company)

    """ def test_threshold_creation(self):
        #Test if a threshold can be created
        self.assertEqual(self.threshold.name, "Test Threshold")
        self.assertEqual(self.threshold.value, 10)
        self.assertEqual(self.threshold.company, self.company)

    def test_threshold_string_representation(self):
        #Test if a threshold is correctly represented as a string
        self.assertEqual(str(self.threshold), "Test Threshold (10) - Test Company")"""
 