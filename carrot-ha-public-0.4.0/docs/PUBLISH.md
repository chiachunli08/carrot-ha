# helico717 계정으로 처음 공개하기

이 폴더의 소스 파일을 GitHub에 올립니다. 개인 PC의 outputs 전체나 DB 파일을 올리는 것이 아닙니다.

1. github.com에서 helico717 계정으로 로그인합니다.
2. 오른쪽 위 + → New repository → 이름 `carrot-ha` → Public → Create repository.
3. GitHub Desktop을 설치하고 같은 계정으로 로그인합니다. File → Clone repository에서 방금 만든 저장소를 선택합니다.
4. 복제한 폴더에 이 배포 폴더의 내용을 복사합니다. 최상단에 README.md, hacs.json, custom_components 폴더가 보여야 합니다.
5. 변경 파일 목록을 검토합니다. connection.json, wrangler.json, DB, 로그, 토큰, 개인 사진/경로가 없어야 합니다.
6. Summary에 `Prepare 0.4.0` → Commit to main → Push origin.
7. GitHub 저장소의 Actions 결과를 확인합니다. 실패가 있으면 공개 릴리스 전에 수정합니다.
8. Releases → Draft a new release → 새 태그 `v0.4.0`, 제목 `Carrot HA 0.4.0`. 변경 내용과 미검증 차량 조건을 적고 최초 릴리스는 pre-release로 검증한 뒤 정식 공개합니다.

HACS 사용자들은 저장소 주소를 Custom repositories에 추가해 설치합니다. HACS 기본 목록에 등재되는 것과 별개입니다.

## 다음 업데이트

소스를 수정하고 manifest.json의 version을 예: 0.4.1로 올립니다. 테스트 후 Commit → Push → 새 Release `v0.4.1`을 발행합니다. HACS가 조회한 뒤 업데이트를 제공하며 사용자가 설치합니다. 콤마/Cloudflare 변경이 있으면 별도 절차를 릴리스 설명에 반드시 적습니다.

공식 요구사항: https://hacs.xyz/docs/publish/integration/
브랜드 아이콘: https://developers.home-assistant.io/docs/core/integration/brand_images/
