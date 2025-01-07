Dưới đây là bản dịch sang tiếng Việt của bài viết "Semantic Search Thesis":

# Luận Văn Tìm Kiếm Ngữ Nghĩa

## Tổng Quan

Dự án Tìm Kiếm Ngữ Nghĩa nhằm nâng cao khả năng tìm kiếm truyền thống bằng cách tích hợp hiểu biết ngữ nghĩa, cho phép truy xuất thông tin chính xác và nhận thức ngữ cảnh hơn. Hệ thống này được thiết kế để xử lý và lập chỉ mục khối lượng dữ liệu lớn, cho phép kết quả tìm kiếm hiệu quả và có ý nghĩa.

- [Luận Văn Tìm Kiếm Ngữ Nghĩa](#luận-văn-tìm-kiếm-ngữ-nghĩa)
    - [Tổng Quan](#tổng-quan)
    - [Các Thành Phần](#các-thành-phần)
        - [1. Quy Trình Tiếp Nhận Dữ Liệu](#1-quy-trình-tiếp-nhận-dữ-liệu)
        - [2. Quy Trình Tìm Kiếm](#2-quy-trình-tìm-kiếm)
        - [3. Đánh Giá](#3-đánh-giá)
        - [4. Phân Loại Truy Vấn](#4-phân-loại-truy-vấn)
        - [5. Điều Phối Quy Trình](#5-điều-phối-quy-trình)
        - [6. Lưu Trữ Dữ Liệu](#6-lưu-trữ-dữ-liệu)
    - [Tổng Quan Dự Án](#tổng-quan-dự-án)
        - [Cấu Trúc Dự Án](#cấu-trúc-dự-án)
        - [Yêu Cầu Tiền Đề](#yêu-cầu-tiền-đề)
        - [Cài Đặt Phụ Thuộc](#cài-đặt-phụ-thuộc)
        - [Chạy Dự Án](#chạy-dự-án)
        - [Kiểm Tra Dự Án](#kiểm-tra-dự-án)
    - [So Sánh Giữa Các Phương Pháp](#so-sánh-giữa-các-phương-pháp)
        - [1. Tìm Kiếm](#1-tìm-kiếm)
        - [2. Lưu Trữ Embedding](#2-lưu-trữ-embedding)
        - [3. Các Chỉ Số](#3-các-chỉ-số)
        - [4. Chiến Lược Tìm Kiếm](#4-chiến-lược-tìm-kiếm)
    - [Mở Rộng](#mở-rộng)

## Các Thành Phần

### 1. Quy Trình Tiếp Nhận Dữ Liệu

Quy trình tiếp nhận dữ liệu rất quan trọng để thu thập và chuẩn bị dữ liệu thô cho tìm kiếm ngữ nghĩa. Nó bao gồm một số quy trình chính:

- **Kết Nối**: Đây là các mô-đun chuyên biệt được thiết kế để giao tiếp với các nguồn dữ liệu khác nhau. Các kết nối hiện tại bao gồm:
    - **Kết Nối Dataset Hugging Face**: Truy xuất dữ liệu trực tiếp từ các dataset của Hugging Face, cho phép tích hợp liền mạch với nhiều dataset có sẵn.
    - **Kết Nối SQL**: Trích xuất dữ liệu từ các cơ sở dữ liệu SQL, cho phép hệ thống truy cập dữ liệu có cấu trúc được lưu trữ trong các cơ sở dữ liệu quan hệ.
    - **Kết Nối Tệp**: Xử lý trích xuất dữ liệu từ các hệ thống tệp cục bộ hoặc trên đám mây, hỗ trợ các định dạng như CSV, JSON, và nhiều hơn nữa.

- **Trích Xuất Dữ Liệu**: Khi dữ liệu được truy xuất qua các kết nối, nó được chuyển đổi thành cấu trúc Tài Liệu chuẩn hóa. Cấu trúc này tạo điều kiện cho việc xử lý và lập chỉ mục nhất quán trên các loại và nguồn dữ liệu khác nhau.

- **Phân Mảnh Ngữ Nghĩa**: Cấu trúc Tài Liệu được chia thành các mảnh nhỏ hơn, có ý nghĩa ngữ nghĩa. Độ chi tiết này nâng cao khả năng của hệ thống trong việc xử lý và lập chỉ mục dữ liệu chính xác, cải thiện độ chính xác của kết quả tìm kiếm.

- **Tạo Embedding**: Mỗi mảnh văn bản được chuyển đổi thành một biểu diễn vector bằng cách sử dụng các kỹ thuật embedding tiên tiến (ví dụ: [Sentence Transformer - paraphrase-mpnet-base-v2](https://huggingface.co/sentence-transformers/paraphrase-mpnet-base-v2)). Các embedding này nắm bắt ý nghĩa ngữ nghĩa của văn bản, cho phép hệ thống hiểu ngữ cảnh và mối quan hệ giữa các mảnh thông tin khác nhau.

- **Lập Chỉ Mục**:
    - **Chỉ Mục Đảo Ngược**: Một phương pháp lập chỉ mục truyền thống ánh xạ các từ khóa đến vị trí của chúng trong tập tài liệu, cho phép tìm kiếm nhanh chóng dựa trên từ khóa.
    - **Chỉ Mục Ngữ Nghĩa**: Chỉ mục này sử dụng các embedding ngữ nghĩa để ánh xạ các truy vấn đến các mảnh tài liệu liên quan dựa trên ý nghĩa thay vì chỉ từ khóa.

### 2. Quy Trình Tìm Kiếm

Quy trình tìm kiếm tích hợp cả `Chỉ Mục Đảo Ngược` và `Chỉ Mục Ngữ Nghĩa` để truy xuất tài liệu liên quan một cách hiệu quả, cho phép người dùng chọn từ các chiến lược khác nhau để nâng cao độ chính xác và liên quan của tìm kiếm.

- **Tìm Kiếm Kết Hợp**:
    - **Chỉ Mục Đảo Ngược**: Nhanh chóng lọc tài liệu bằng cách khớp từ khóa cho các truy vấn đơn giản.
    - **Chỉ Mục Ngữ Nghĩa**: Xếp hạng lại kết quả bằng cách hiểu ngữ cảnh và ý nghĩa của truy vấn để có tài liệu liên quan hơn.

- **Cơ Chế Dự Phòng**:
    - **Chỉ Mục Ngữ Nghĩa Trước**: Ưu tiên độ liên quan cao và hiểu biết ngữ cảnh.
    - **Dự Phòng cho Chỉ Mục Đảo Ngược**: Chuyển sang tìm kiếm dựa trên từ khóa nếu cần.

- **Tìm Kiếm Phân Tầng**:
    - Phân loại truy vấn thành đơn giản hoặc phức tạp.
    - **Chỉ Mục Đảo Ngược**: Được sử dụng cho các truy vấn đơn giản với khớp từ khóa.
    - **Chỉ Mục Ngữ Nghĩa**: Được sử dụng cho các truy vấn phức tạp để nắm bắt ý định của người dùng và cung cấp kết quả chính xác.

Sơ Đồ Tìm Kiếm

![search-diagram](docs/semantic-search-diagram-20250103.png)

### 3. Đánh Giá

Hiệu suất của hệ thống được đánh giá bằng cách sử dụng [dataset MS MARCO](https://huggingface.co/datasets/microsoft/ms_marco/viewer/v1.1/train), một tiêu chuẩn cho đọc hiểu máy và xếp hạng đoạn văn:

- **Dataset MS MARCO**: Chứa các truy vấn thực tế của người dùng và các đoạn văn liên quan, cung cấp một môi trường thử nghiệm thực tế để đánh giá các hệ thống tìm kiếm.

- **Tính Toán Chỉ Số**:
    - **Precision@k**: Đo lường tỷ lệ tài liệu liên quan trong top `k` kết quả, chỉ ra khả năng của hệ thống trong việc ưu tiên thông tin liên quan.
    - **MRR@10 (Mean Reciprocal Rank at 10)**: Đánh giá chất lượng xếp hạng bằng cách xem xét vị trí của tài liệu liên quan đầu tiên trong top 10 kết quả.

### 4. Phân Loại Truy Vấn

Trong cách tiếp cận `Tìm Kiếm Phân Tầng`, việc phân biệt chính xác giữa các truy vấn đơn giản và phức tạp là rất quan trọng để nâng cao độ chính xác của tìm kiếm. Sử dụng [dataset MS MARCO](https://huggingface.co/datasets/microsoft/ms_marco/viewer/v1.1/train), các truy vấn được phân loại dựa trên cột `query_type`:

- **Truy Vấn Đơn Giản**: Được gắn nhãn là `description`.
- **Truy Vấn Phức Tạp**: Bao gồm `entity`, `location`, `numeric`, và các loại khác.

**Phương Pháp**:

- **Chuẩn Bị Dữ Liệu**: Token hóa và nhúng các truy vấn bằng tokenizer của mô hình `paraphrase-mpnet-base-v2`.
- **Huấn Luyện Mô Hình**: Tinh chỉnh một mô hình phân loại chuỗi để dự đoán nhãn nhị phân, phân biệt giữa các truy vấn đơn giản và phức tạp.
- **Đánh Giá**: Đánh giá hiệu suất của mô hình bằng cách sử dụng tập kiểm tra từ dataset MS MARCO.

**Kết Quả**:

- Mô hình phân loại hiệu quả độ phức tạp của truy vấn bằng cách sử dụng các embedding ngữ nghĩa, nâng cao hệ thống tìm kiếm phân tầng.

### 5. Điều Phối Quy Trình

Hệ thống sử dụng [Prefect](https://www.prefect.io/) để quản lý các quy trình, đảm bảo thực thi hiệu quả và đáng tin cậy của các nhiệm vụ:

- **Luồng**: Đại diện cho toàn bộ quy trình, bao gồm tiếp nhận dữ liệu, tìm kiếm, và các vòng phản hồi.
- **Nhiệm Vụ**: Các thành phần riêng lẻ của luồng, như phân mảnh ngữ nghĩa, tạo embedding, mở rộng truy vấn, và phân loại truy vấn.

### 6. Lưu Trữ Dữ Liệu

Các giải pháp lưu trữ dữ liệu hiệu quả được sử dụng để xử lý cả dữ liệu thô và đã xử lý:

- **Lưu Trữ Tài Liệu Thô**: [MongoDB](https://www.mongodb.com/) được sử dụng để lưu trữ các tài liệu chưa xử lý, cung cấp một giải pháp cơ sở dữ liệu linh hoạt và có thể mở rộng.
- **Lưu Trữ Dữ Liệu Đã Xử Lý**: [Elasticsearch](https://www.elastic.co/elasticsearch) được sử dụng để lưu trữ dữ liệu đã xử lý và lập chỉ mục, cho phép các hoạt động tìm kiếm nhanh chóng và hiệu quả.

## Tổng Quan Dự Án

### Cấu Trúc Dự Án

```plaintext
semantic-search/
│
├── data/
│   ├── raw/                     # Tài liệu thô
│   ├── processed/               # Tài liệu đã xử lý và phân mảnh
│
├── src/
│   ├── __init__.py
│   ├── ingest.py                # Luồng tiếp nhận
│   ├── chunking.py              # Phân mảnh ngữ nghĩa
│   ├── embedding.py             # Tạo embedding
│   ├── search.py                # Logic tìm kiếm kết hợp
│   ├── query_expansion.py       # Logic mở rộng truy vấn
│   ├── query_classification.py  # Logic phân loại truy vấn
│   ├── evaluation.py            # Chỉ số đánh giá
│   ├── database.py              # Tương tác cơ sở dữ liệu
│   ├── flow.py                  # Luồng Prefect
│
├── requirements.txt             # Phụ thuộc Python
├── main.py                      # Điểm vào chính
└── README.md
```

### Yêu Cầu Tiền Đề

- **Docker**: Cần thiết để chạy các dịch vụ bên thứ ba như Elasticsearch và Postgres.
- **Phiên bản Python**: 3.12

### Cài Đặt Phụ Thuộc

Để thiết lập môi trường dự án, chạy script sau:

```bash
bash scripts/setup.sh
```

### Chạy Dự Án

Để bắt đầu dự án, thực hiện:

```bash
bash scripts/start.sh
```

### Kiểm Tra Dự Án

Để kiểm tra chức năng của dự án, sử dụng:

```bash
bash scripts/test.sh
```

## So Sánh Giữa Các Phương Pháp

Dự án này đánh giá các phương pháp tìm kiếm và lập chỉ mục khác nhau, nêu bật ưu và nhược điểm của chúng.

### 1. Tìm Kiếm

- **Elastic Search**: Hỗ trợ xếp hạng phức tạp và các thao tác CRUD, lý tưởng cho các ứng dụng quy mô lớn. Cho phép lưu trữ phân tán, hỗ trợ mở rộng.
- **FAISS**: Cung cấp xử lý nhanh trong bộ nhớ, hoàn hảo cho việc xử lý hiệu quả các tập dữ liệu lớn, nhưng thiếu hỗ trợ CRUD và lưu trữ bền vững.
- **TF-IDF**: Dễ triển khai nhưng chậm đối với các tập dữ liệu lớn do tính toán thời gian chạy.

### 2. Lưu Trữ Embedding

- **Cơ Sở Dữ Liệu Vector**: Tối ưu hóa cho việc lưu trữ và truy vấn các vector có chiều cao, cung cấp tìm kiếm tương tự hiệu quả.
- **Elastic-Search KNN-plugin**: Tích hợp liền mạch với các thiết lập Elastic Search hiện có, cho phép tìm kiếm k-láng giềng gần nhất hiệu quả.

### 3. Các Chỉ Số

- **Precision@k, MRR@10**: Tập trung vào độ chính xác và chất lượng xếp hạng của những kết quả đầu tiên, rất quan trọng cho các ứng dụng như chatbot nơi phản hồi đầu tiên thường là quan trọng nhất.
- **Recall@k**: Đo lường khả năng truy xuất tất cả các tài liệu liên quan trong top k kết quả, nêu bật tính toàn diện của hệ thống.
- **F1-Score**: Cân bằng giữa độ chính xác và độ nhớ, cung cấp một chỉ số duy nhất để đánh giá hiệu suất tìm kiếm tổng thể.

### 4. Chiến Lược Tìm Kiếm

- **Tìm Kiếm Kết Hợp**: Cách tiếp cận này tối ưu hóa chi phí bằng cách lọc kết quả ban đầu bằng tìm kiếm từ khóa trước khi áp dụng xếp hạng ngữ nghĩa. Tuy nhiên, hạn chế của nó nằm ở khả năng thất bại của tìm kiếm từ khóa trong việc xử lý các truy vấn phức tạp, có thể dẫn đến dữ liệu không đủ cho xếp hạng hiệu quả.
- **Tìm Kiếm Phân Tầng**: Cân bằng giữa hiệu quả và độ chính xác bằng cách phân loại truy vấn thành các loại đơn giản và phức tạp, áp dụng tìm kiếm từ khóa cho các truy vấn đơn giản và tìm kiếm ngữ nghĩa cho những truy vấn phức tạp hơn.
- **Cơ Chế Dự Phòng**: Ưu tiên độ chính xác cao bằng cách bắt đầu với tìm kiếm ngữ nghĩa, nhưng điều này có thể tốn kém về mặt tính toán. Nếu tìm kiếm ngữ nghĩa không mang lại kết quả thỏa đáng, nó sẽ dự phòng sang các phương pháp dựa trên từ khóa để đảm bảo độ bao phủ tìm kiếm toàn diện.

## Mở Rộng

Dự án nêu ra các lĩnh vực tiềm năng để mở rộng và cải thiện:

- **Kết Nối**: Phát triển thêm các kết nối để tích hợp với các nguồn dữ liệu khác nhau.
- **Phản Hồi Của Người Dùng**: Tích hợp phản hồi của người dùng để cải thiện độ chính xác và liên quan của tìm kiếm.
- **Xếp Hạng Phức Tạp**:
    - Nâng cao các thuật toán xếp hạng bằng cách kết hợp các yếu tố như ngữ nghĩa, ngày phát hành, ngày hiệu lực, và các đối tượng áp dụng.
    - Sử dụng tìm kiếm ngữ nghĩa tích hợp sẵn của Elasticsearch với cross-encoder để cải thiện độ liên quan.
- **Tăng Tốc Xử Lý Trên GPU**:
    - Sử dụng GPU để tăng tốc độ xử lý.
    - Thực hiện các tính toán tương tự trong Elasticsearch bằng CPU theo mặc định.
- **Ứng Dụng Thực Tế**: Sử dụng tìm kiếm ngữ nghĩa để tổng hợp dữ liệu từ `các nguồn đa dạng`, cải thiện tương tác người dùng trên các lĩnh vực:
    - **Phân Tích Yêu Cầu**: Cải thiện tích hợp và hiểu biết về các yêu cầu kinh doanh, sản phẩm, và kỹ thuật.
    - **Hỗ Trợ Khách Hàng**: Khớp chính xác các yêu cầu của người dùng với các giải pháp bằng cách hiểu ngữ nghĩa của các truy vấn.
    - **Phân Tích Pháp Lý**: Cho phép tìm kiếm và phân tích ngữ cảnh hiệu quả các tài liệu pháp lý.
