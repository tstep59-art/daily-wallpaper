Feature: 픽셀아트 프롬프트 조립
  풍경 중심의 고품질 16-bit 픽셀아트에 명승지, 계절, 날씨, 시간대를 반영한다.

  Scenario Outline: 날짜로 계절을 정한다
    When 날짜 <date> 의 계절을 구한다
    Then 계절은 "<season>" 이다

    Examples:
      | date       | season |
      | 2026-03-01 | spring |
      | 2026-05-31 | spring |
      | 2026-06-01 | summer |
      | 2026-08-31 | summer |
      | 2026-09-01 | autumn |
      | 2026-11-30 | autumn |
      | 2026-12-01 | winter |
      | 2027-02-28 | winter |

  Scenario: 모든 프롬프트는 세밀한 16비트 픽셀아트다
    Given 박연폭포 명승지
    When day 시간대, autumn 계절, clear 날씨로 프롬프트를 만든다
    Then 프롬프트에 "16-bit pixel art" 가 들어 있다
    And 프롬프트에 "Vertical 9:16 smartphone wallpaper" 가 들어 있다
    And 프롬프트에 "no text" 가 들어 있다

  Scenario: 풍경이 화면 대부분을 차지한다
    Given 박연폭포 명승지
    When day 시간대, autumn 계절, clear 날씨로 프롬프트를 만든다
    Then 프롬프트에 "80 to 90 percent" 가 들어 있다
    And 프롬프트에 "no large characters" 가 들어 있다

  Scenario: 명승지 묘사가 들어간다
    Given 박연폭포 명승지
    When day 시간대, autumn 계절, clear 날씨로 프롬프트를 만든다
    Then 프롬프트에 "waterfall plunging" 가 들어 있다

  Scenario: 계절과 날씨가 프롬프트에 반영된다
    Given 박연폭포 명승지
    When day 시간대, winter 계절, snow 날씨로 프롬프트를 만든다
    Then 프롬프트에 "winter scenery" 가 들어 있다
    And 프롬프트에 "gentle snowfall" 가 들어 있다

  Scenario: 모든 날씨 상태와 시간대와 계절 조합에 문구가 준비되어 있다
    Given 박연폭포 명승지
    Then 모든 조합으로 프롬프트를 만들 수 있다

  Scenario: 어떤 조합도 프롬프트 길이 제한을 넘지 않는다
    Given 실제 명승지 데이터 파일
    Then 모든 명승지와 조합의 프롬프트가 2000자 이하이다

  Scenario: 어떤 조합에도 색 이름이 들어가지 않는다
    Given 실제 명승지 데이터 파일
    Then 모든 명승지와 조합의 프롬프트에 색 이름이 없다

  Scenario: 알 수 없는 시간대는 거부된다
    Given 박연폭포 명승지
    When dawn 시간대, autumn 계절, clear 날씨로 프롬프트를 만들려 한다
    Then 프롬프트 입력 오류가 발생한다

  Scenario: 알 수 없는 날씨 상태는 거부된다
    Given 박연폭포 명승지
    When day 시간대, autumn 계절, hail 날씨로 프롬프트를 만들려 한다
    Then 프롬프트 입력 오류가 발생한다
