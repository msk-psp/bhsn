# Project Brief: 법령 정보 관리 데이터 파이프라인 및 API 서버

## Executive Summary

본 프로젝트는 법제처에서 제공하는 API를 통해 법령 및 조항 데이터를 수집, 관리하는 데이터 파이프라인과, 정제된 데이터를 외부에 제공하는 API 서버를 구축하는 것을 목표로 합니다. Apache Airflow를 사용한 주기적인 배치 파이프라인을 통해 데이터의 정합성과 최신성을 보장하고, FastAPI 기반의 API 서버를 통해 안정적인 데이터 서비스를 제공합니다. 이 시스템은 데이터 파이프라인과 API 서버가 분리된 아키텍처를 채택하여 확장성과 유지보수성을 높입니다.

## Problem Statement

현재 법령 데이터는 파편화되어 있고, 최신 상태를 유지하며 데이터 간의 관계(법령-조항)를 정확히 관리하는 데 어려움이 있습니다. 이로 인해 개발자나 데이터 소비자는 신뢰할 수 있는 최신 법령 데이터를 안정적으로 활용하기 어렵습니다. 데이터 파이프라인의 부재는 주기적인 데이터 업데이트, 데이터 정합성 유지, 그리고 장애 발생 시 신속한 대응을 어렵게 만드는 핵심 문제입니다.

## Proposed Solution

이 문제 해결을 위해, 데이터 수집/처리를 담당하는 **배치 파이프라인**과 데이터 제공을 담당하는 **API 서버**를 분리한 아키텍처를 제안합니다.

*   **데이터 파이프라인**: Apache Airflow를 사용하여 매일 정해진 시간에 Mock 법령 API로부터 데이터를 수집, 정제하여 MySQL 데이터베이스에 적재합니다. 파이프라인의 모든 태스크는 멱등성을 보장하여 실패 시 재시도에 대한 안정성을 확보합니다.
*   **API 서버**: FastAPI를 사용하여 구축된 RESTful API 서버는 데이터베이스에 저장된 법령 데이터를 외부 클라이언트에게 제공합니다. 서버는 로드 밸런서 뒤에서 다중 인스턴스로 운영되어 무중단 서비스를 지원합니다.
*   **데이터 저장소**: MySQL 데이터베이스를 Primary-Replica 구조로 구성하여 데이터의 가용성과 안정적인 읽기 성능을 보장합니다.

이 솔루션은 저장소 패턴(Repository Pattern)과 의존성 주입(Dependency Injection)을 적용하여 코드의 유지보수성과 테스트 용이성을 높입니다.

## Target Users

*   **Primary User Segment: 내부 개발자 및 데이터 분석가**
    *   **Profile**: 사내 다른 서비스나 시스템을 개발하는 백엔드 개발자 또는 데이터 기반 의사결정을 위해 법령 데이터가 필요한 데이터 분석가.
    *   **Needs**: 항상 최신으로 유지되는 정확한 법령 데이터에 프로그래밍 방식으로 쉽게 접근하기를 원합니다. 안정적이고 문서화가 잘 된 API를 통해 데이터를 빠르고 효율적으로 조회해야 합니다.

## Goals & Success Metrics

### Business Objectives
*   법령 데이터의 중앙 관리 및 최신 상태 유지 자동화
*   안정적이고 예측 가능한 API를 통한 데이터 제공
*   데이터 파이프라인의 효율적인 설계 및 운영

### User Success Metrics
*   개발자가 API를 통해 원하는 법령 및 조항 데이터를 99.9% 이상의 성공률로 조회할 수 있음
*   데이터 파이프라인이 매일 정해진 시간 내에 성공적으로 완료되는 비율 99.5% 이상

### Key Performance Indicators (KPIs)
*   **API 응답 시간**: 평균 200ms 이하
*   **API 가용성**: 99.9% 이상
*   **데이터 최신성**: 데이터베이스의 데이터가 소스 API와 24시간 이내의 차이를 유지
*   **파이프라인 실패 알림 시간**: 실패 발생 후 5분 이내에 관리자에게 알림

## MVP Scope

### Core Features (Must Have)
*   **데이터 파이프라인**:
    *   Mock API(`GET /laws`, `GET /law/{id}`)로부터 법령 및 조항 데이터 수집
    *   수집된 데이터 정제 및 `Law`, `Article` 모델에 맞게 변환
    *   MySQL 데이터베이스에 데이터 저장 (Upsert)
    *   Airflow를 사용한 일일 주기적 실행 스케줄링
    *   파이프라인 실패 시 Mock 알림 API 호출
*   **API 서버**:
    *   `GET /laws`: 전체 법령 목록 조회 API
    *   `GET /laws/{law_id}`: 특정 법령 정보 조회 API
    *   `GET /laws/{law_id}/articles`: 특정 법령의 모든 조문 조회 API
    *   `GET /articles/{article_id}`: 특정 조문 정보 조회 API
*   **데이터베이스**:
    *   `Law` 및 `Article` 테이블 스키마 정의 및 생성

### Out of Scope for MVP
*   사용자 인증 및 인가 기능
*   API 사용량 제한(Rate Limiting) 및 고급 캐싱 전략
*   웹 기반 관리자 대시보드
*   데이터 분석 및 시각화 기능

## Post-MVP Vision

*   **Phase 2 Features**:
    *   실제 법제처 Open API 연동
    *   사용자 인증(API Key) 및 사용량 추적 기능 도입
    *   API 성능 향상을 위한 Redis 캐싱 계층 추가
    *   법령 내용에 대한 전문(Full-text) 검색 기능
*   **Long-term Vision**:
    *   외부 개발자를 위한 공개 API 포털 구축
    *   수집된 데이터를 활용한 법령 개정 이력 추적 및 분석 서비스 제공

## Technical Considerations

*   **Technology Stack**:
    *   **Language**: Python 3.11
    *   **Pipeline**: Apache Airflow 2.8.1
    *   **API**: FastAPI 0.109.2, Uvicorn 0.27.1
    *   **Database**: MySQL 8.0, SQLAlchemy 2.0.25
*   **Architecture**:
    *   데이터 파이프라인과 API 서버가 분리된 서비스 지향 아키텍처
    *   모노레포(Monorepo) 구조 채택
    *   저장소 패턴(Repository Pattern) 및 의존성 주입(Dependency Injection) 적용
*   **Infrastructure**:
    *   Cloud-Agnostic 설계를 지향 (AWS 예시: EC2, RDS, ALB)
    *   Terraform을 사용한 Infrastructure as Code (IaC)
    *   GitHub Actions를 통한 CI/CD 파이프라인 구축

## Constraints & Assumptions

*   **Constraints**:
    *   실제 API 연동 없이 제공된 Mock API 명세를 기반으로 개발해야 함
    *   제출물에는 전체 데이터 파이프라인 설계 문서와 각 컴포넌트별 간단한 구현 스크립트가 포함되어야 함
*   **Key Assumptions**:
    *   Mock API는 항상 안정적으로 응답한다고 가정함
    *   법령 데이터의 양이 일반적인 RDBMS로 처리 가능한 수준이라고 가정함
    *   주요 사용자는 API를 통해 데이터를 소비하는 개발자라고 가정함

## Risks & Open Questions

*   **Key Risks**:
    *   **테스트 전략 부재**: 자동화된 테스트 계획이 없어 코드의 정확성과 안정성을 보장하기 어려움. (아키텍처 문서에서 식별된 위험)
    *   **운영 준비성 부족**: 캐싱, 모니터링 등 실제 운영을 위한 세부 사항이 부족하여 향후 성능 및 장애 대응에 어려움이 있을 수 있음. (아키텍처 문서에서 식별된 위험)
    *   **Mock API와 실제 API의 차이**: 향후 실제 API로 전환 시, 데이터 구조나 인증 방식의 차이로 인해 상당한 재작업이 필요할 수 있음.
*   **Open Questions**:
    *   법령 데이터의 구체적인 양과 증가율은 어느 정도인가?
    *   API의 실시간성이 요구되는 사용 사례가 있는가? (현재는 일 배치 기준)

## Appendices

*   **References**:
    *   Data Engineer 과제.pdf
    *   docs/architecture.md

## Next Steps

1.  **프로젝트 구조 생성**: `docs/architecture.md`의 `Source Tree` 섹션에 따라 프로젝트 디렉터리 및 기본 파일 구조를 생성합니다.
2.  **데이터 모델 구현**: `common/db/models.py`에 SQLAlchemy ORM 모델(`Law`, `Article`)을 정의합니다.
3.  **데이터베이스 스크립트 작성**: `law` 및 `article` 테이블을 생성하는 SQL 스크립트를 작성합니다.
4.  **데이터 파이프라인 구현**: `law_pipeline` 모듈 내에 크롤러, 로더 등 핵심 로직을 구현하고, 이를 바탕으로 Airflow DAG(`dags/law_data_pipeline_dag.py`)를 작성합니다.
5.  **API 서버 구현**: `api_server` 모듈 내에 FastAPI 애플리케이션과 각 API 라우터를 구현합니다.
