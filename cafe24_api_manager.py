"""
Cafe24 API Manager for Pooweep Pet Store
=========================================
Cafe24 Open API를 활용한 상품/주문/고객 자동화 관리 스크립트

사용법:
    1. .env 파일에 API 키 설정
        2. python cafe24_api_manager.py

        필요 패키지: pip install requests python-dotenv schedule
        """

import os
import json
import time
import logging
import requests
import schedule
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
      level=logging.INFO,
      format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
      handlers=[
                logging.FileHandler('pooweep_automation.log', encoding='utf-8'),
                logging.StreamHandler()
      ]
)
logger = logging.getLogger('PooweepAutomation')


class Cafe24APIManager:
      """Cafe24 Open API v2 매니저"""

    BASE_URL = "https://pooweep.cafe24api.com/api/v2"

    def __init__(self):
              self.client_id = os.getenv('CAFE24_CLIENT_ID')
              self.client_secret = os.getenv('CAFE24_CLIENT_SECRET')
              self.access_token = os.getenv('CAFE24_ACCESS_TOKEN')
              self.refresh_token = os.getenv('CAFE24_REFRESH_TOKEN')
              self.mall_id = os.getenv('CAFE24_MALL_ID', 'pooweep')
              self.shop_no = 1

    @property
    def headers(self):
              return {
                            'Authorization': f'Bearer {self.access_token}',
                            'Content-Type': 'application/json',
                            'X-Cafe24-Api-Version': '2024-06-01'
              }

    def refresh_access_token(self):
              """액세스 토큰 갱신"""
              url = f"https://{self.mall_id}.cafe24api.com/api/v2/oauth/token"
              data = {
                  'grant_type': 'refresh_token',
                  'refresh_token': self.refresh_token
              }
              resp = requests.post(url, data=data, auth=(self.client_id, self.client_secret))
              if resp.status_code == 200:
                            tokens = resp.json()
                            self.access_token = tokens['access_token']
                            self.refresh_token = tokens['refresh_token']
                            logger.info("토큰 갱신 성공")
                            return True
                        logger.error(f"토큰 갱신 실패: {resp.text}")
        return False

    # ==================== 상품 관리 ====================

    def get_products(self, limit=100, offset=0, category_id=None):
              """상품 목록 조회"""
        params = {'shop_no': self.shop_no, 'limit': limit, 'offset': offset}
        if category_id:
                      params['category'] = category_id
                  resp = requests.get(f"{self.BASE_URL}/admin/products", headers=self.headers, params=params)
        return resp.json() if resp.status_code == 200 else None

    def get_product(self, product_no):
              """상품 상세 조회"""
        resp = requests.get(f"{self.BASE_URL}/admin/products/{product_no}", headers=self.headers)
        return resp.json() if resp.status_code == 200 else None

    def update_product(self, product_no, data):
              """상품 정보 수정"""
        payload = {'shop_no': self.shop_no, 'request': data}
        resp = requests.put(
                      f"{self.BASE_URL}/admin/products/{product_no}",
                      headers=self.headers,
                      json=payload
        )
        return resp.json() if resp.status_code == 200 else None

    def get_categories(self):
              """상품 분류 목록 조회"""
        resp = requests.get(
                      f"{self.BASE_URL}/admin/categories",
                      headers=self.headers,
                      params={'shop_no': self.shop_no}
        )
        return resp.json() if resp.status_code == 200 else None

    # ==================== 주문 관리 ====================

    def get_orders(self, start_date=None, end_date=None, status=None):
              """주문 목록 조회"""
        if not start_date:
                      start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
                  if not end_date:
                                end_date = datetime.now().strftime('%Y-%m-%d')
                            params = {
                                          'shop_no': self.shop_no,
                                          'start_date': start_date,
                                          'end_date': end_date,
                                          'limit': 100
                            }
        if status:
                      params['order_status'] = status
                  resp = requests.get(f"{self.BASE_URL}/admin/orders", headers=self.headers, params=params)
        return resp.json() if resp.status_code == 200 else None

    def update_order_status(self, order_id, status):
              """주문 상태 변경 (N10=입금전, N20=입금완료, N30=배송준비중, N40=배송중, N50=배송완료)"""
        payload = {'shop_no': self.shop_no, 'request': {'order_status': status}}
        resp = requests.put(
                      f"{self.BASE_URL}/admin/orders/{order_id}",
                      headers=self.headers,
                      json=payload
        )
        return resp.json() if resp.status_code == 200 else None

    # ==================== 고객 관리 ====================

    def get_customers(self, limit=100):
              """회원 목록 조회"""
        resp = requests.get(
                      f"{self.BASE_URL}/admin/customers",
                      headers=self.headers,
                      params={'shop_no': self.shop_no, 'limit': limit}
        )
        return resp.json() if resp.status_code == 200 else None

    # ==================== 재고 관리 ====================

    def check_low_stock(self, threshold=5):
              """재고 부족 상품 확인"""
        products = self.get_products(limit=100)
        if not products:
                      return []
                  low_stock = []
        for p in products.get('products', []):
                      if p.get('stock_quantity', 0) <= threshold:
                                        low_stock.append({
                                                              'product_no': p['product_no'],
                                                              'product_name': p['product_name'],
                                                              'stock': p.get('stock_quantity', 0)
                                        })
                                return low_stock

    # ==================== 자동화 작업 ====================

    def daily_report(self):
              """일일 리포트 생성"""
        logger.info("=== 일일 리포트 시작 ===")
        orders = self.get_orders()
        order_count = len(orders.get('orders', [])) if orders else 0
        low_stock = self.check_low_stock()
        report = {
                      'date': datetime.now().strftime('%Y-%m-%d'),
                      'new_orders': order_count,
                      'low_stock_items': len(low_stock),
                      'low_stock_details': low_stock
        }
        logger.info(f"신규주문: {order_count}건, 재고부족: {len(low_stock)}건")
        with open(f"reports/daily_{report['date']}.json", 'w', encoding='utf-8') as f:
                      json.dump(report, f, ensure_ascii=False, indent=2)
        return report

    def auto_process_orders(self):
              """자동 주문 처리 (입금확인 -> 배송준비중)"""
        orders = self.get_orders(status='N20')
        if not orders:
                      return
        for order in orders.get('orders', []):
                      result = self.update_order_status(order['order_id'], 'N30')
            if result:
                              logger.info(f"주문 {order['order_id']} -> 배송준비중 처리완료")


def run_scheduler():
      """스케줄러 실행"""
    manager = Cafe24APIManager()

    schedule.every().day.at("09:00").do(manager.daily_report)
    schedule.every(30).minutes.do(manager.auto_process_orders)
    schedule.every(2).hours.do(manager.refresh_access_token)

    logger.info("Pooweep 자동화 스케줄러 시작")
    while True:
              schedule.run_pending()
        time.sleep(60)


if __name__ == '__main__':
      os.makedirs('reports', exist_ok=True)
    run_scheduler()
