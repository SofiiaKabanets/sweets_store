from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from vouchers.models import Voucher


class VoucherApplyViewTest(TestCase):
    def setUp(self):
        self.voucher = Voucher.objects.create(
            code='111',
            valid_from=timezone.now(),
            valid_to=timezone.now(),
            discount=10,
            active=True
        )
        self.url = reverse('vouchers:apply')

    def test_invalid_voucher_application(self):
        response = self.client.post(self.url, {'code': 'INVALID'})
        self.assertEqual(response.status_code, 302)

        self.assertIsNone(self.client.session.get('voucher_id'))
