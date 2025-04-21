from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        if idx in self.istasyonlar:
            print(f"Hata: {idx} ID'li istasyon zaten mevcut!")
            return
        istasyon = Istasyon(idx, ad, hat)
        self.istasyonlar[idx] = istasyon
        self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        if istasyon1_id not in self.istasyonlar or istasyon2_id not in self.istasyonlar:
            print(f"Hata: {istasyon1_id} veya {istasyon2_id} ID'li istasyon bulunamadı!")
            return
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)

    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            print("Hata: Başlangıç veya hedef istasyonu mevcut değil!")
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        kuyruk = deque([(baslangic, [baslangic])])
        ziyaret_edildi = set()

        while kuyruk:
            mevcut, yol = kuyruk.popleft()

            if mevcut == hedef:
                return yol

            if mevcut in ziyaret_edildi:
                continue

            ziyaret_edildi.add(mevcut)

            for komsu, _ in mevcut.komsular:
                if komsu not in ziyaret_edildi:
                    kuyruk.append((komsu, yol + [komsu]))

        print("Hata: Hedefe ulaşan bir rota bulunamadı!")
        return None

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            print("Hata: Başlangıç veya hedef istasyonu mevcut değil!")
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        pq = [(0, id(baslangic), baslangic, [baslangic])]
        ziyaret_edildi = {}

        while pq:
            sure, _, mevcut, yol = heapq.heappop(pq)

            if mevcut == hedef:
                return yol, sure

            if mevcut in ziyaret_edildi and ziyaret_edildi[mevcut] <= sure:
                continue

            ziyaret_edildi[mevcut] = sure

            for komsu, gecis_suresi in mevcut.komsular:
                heapq.heappush(pq, (sure + gecis_suresi, id(komsu), komsu, yol + [komsu]))

        print("Hata: Hedefe ulaşan bir rota bulunamadı!")
        return None

# Test fonksiyonları
def test_metro():
    metro = MetroAgi()

    metro.istasyon_ekle("A", "Istasyon A", "Hat 1")
    metro.istasyon_ekle("B", "Istasyon B", "Hat 1")
    metro.istasyon_ekle("C", "Istasyon C", "Hat 2")
    metro.baglanti_ekle("A", "B", 5)
    metro.baglanti_ekle("B", "C", 7)

    print("\nEn az aktarmalı rota:")
    rota = metro.en_az_aktarma_bul("A", "C")
    if rota:
        print(" -> ".join(i.ad for i in rota))
    else:
        print("Rota bulunamadı.")

    print("\nEn hızlı rota:")
    sonuc = metro.en_hizli_rota_bul("A", "C")
    if sonuc:
        rota, sure = sonuc
        print(f"{sure} dakika: " + " -> ".join(i.ad for i in rota))
    else:
        print("Rota bulunamadı.")

if __name__ == "__main__":
    test_metro()