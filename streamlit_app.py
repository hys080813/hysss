import streamlit as st
import math

def calculate_geometric_ratio(first_term, nth_term, n):
    """
    등비수열의 첫째 항, n번째 항, 그리고 n을 입력받아 공비를 계산합니다.

    Args:
        first_term (float): 등비수열의 첫째 항 (a1).
        nth_term (float): 등비수열의 n번째 항 (an).
        n (int): n번째 항의 위치 (n은 1보다 커야 합니다).

    Returns:
        float: 등비수열의 공비 (r).
        str: 오류 메시지 (유효하지 않은 입력의 경우).
    """
    if n <= 1:
        return "n은 1보다 큰 정수여야 합니다. (첫째 항과 n번째 항이 같을 수 없습니다.)"
    if first_term == 0:
        # 첫째 항이 0일 때, n번째 항도 0이면 공비는 정의할 수 없음 (0, 0, 0, ... 또는 0, 0, 0, 5, ... 등)
        if nth_term == 0:
            return "첫째 항과 n번째 항이 모두 0이면 공비를 특정할 수 없습니다."
        # 첫째 항만 0이면 공비는 정의할 수 없음 (0, r*0, r^2*0... 인데 0이 아닌 an이 나올 수 없음)
        return "첫째 항은 0이 될 수 없습니다."
    
    # an / a1 값이 음수인데 (n-1)이 짝수일 경우 실수 공비는 존재하지 않음 (예: r^2 = -4)
    if (nth_term / first_term) < 0 and (n - 1) % 2 == 0:
        return "음수의 짝수 제곱근은 실수 공비를 계산할 수 없습니다. (공비가 복소수가 될 수 있습니다.)"

    try:
        # n번째 항이 0이고 첫째 항이 0이 아닐 경우 공비는 0 (예: 5, 0, 0, ...)
        if nth_term == 0 and first_term != 0:
            return 0.0
        
        # 일반적인 공비 계산 공식
        ratio_raw = (nth_term / first_term)**(1 / (n - 1))
        
        # 부동소수점 오차로 인한 미세한 값 조정 (0에 가까운 값은 0으로 처리)
        if abs(ratio_raw) < 1e-9: # 0.000000001보다 작으면 0으로 간주
            ratio = 0.0
        else:
            ratio = ratio_raw
            
        return ratio
    except ZeroDivisionError:
        # 이 예외는 first_term이 0일 때 주로 발생하며, 이미 위에서 처리됨
        return "계산 중 0으로 나누는 오류가 발생했습니다. (입력값을 다시 확인해주세요.)"
    except OverflowError:
        return "계산 결과가 너무 커서 표현할 수 없습니다. 입력 값을 줄여주세요."
    except Exception as e:
        return f"공비 계산 중 알 수 없는 오류가 발생했습니다: {e}"

# --- 스트림릿 앱 UI 구성 시작 ---

# 페이지의 제목과 레이아웃 설정
st.set_page_config(page_title="등비수열 공비 계산기", layout="centered")

# 앱의 메인 제목과 설명
st.title("🔢 등비수열 공비 계산기")
st.markdown("첫째 항 ($a_1$)과 $n$번째 항 ($a_n$)의 값을 입력하여 등비(공비)를 계산합니다.")

# 사이드바에 입력 위젯 배치
st.sidebar.header("값 입력")
# number_input 위젯으로 숫자 입력 받기
a1 = st.sidebar.number_input("첫째 항 ($a_1$)", value=1.0, step=0.1, format="%.2f", help="등비수열의 첫 번째 값입니다.")
an = st.sidebar.number_input("$n$번째 항 ($a_n$)", value=2.0, step=0.1, format="%.2f", help="알고 있는 특정 항의 값입니다.")
n = st.sidebar.number_input("몇 번째 항입니까? ($n$)", value=2, min_value=2, step=1, help="입력한 $n$번째 항의 순서입니다 (최소 2).")

# 계산 버튼
if st.sidebar.button("공비 계산하기"):
    # n 값에 대한 추가적인 유효성 검사 (함수 내부에서도 하지만, UI에서 바로 피드백)
    if n <= 1:
        st.error("오류: $n$은 1보다 큰 정수여야 합니다. 2 이상의 값을 입력해 주세요.")
    else:
        # calculate_geometric_ratio 함수를 호출하여 공비 계산 시도
        result = calculate_geometric_ratio(a1, an, n)
        
        # 함수의 반환 값에 따라 결과 또는 오류 메시지 표시
        if isinstance(result, str): # 반환 값이 문자열이면 오류 메시지
            st.error(f"오류: {result}")
        else: # 반환 값이 숫자(float)이면 성공적으로 공비 계산
            st.success(f"계산된 공비 ($r$)는 **{result:.6f}** 입니다.") # 소수점 6자리까지 표시
            
            # 계산 결과 검증 섹션
            st.subheader("계산 확인")
            st.markdown(f"**입력된 값:**")
            st.markdown(f"- 첫째 항 $a_1 = {a1}$")
            st.markdown(f"- $n$번째 항 $a_n = {an}$")
            st.markdown(f"- $n = {n}$")
            st.markdown(f"**계산된 공비 $r = {result:.6f}$**")
            
            # 계산된 공비로 n번째 항을 다시 계산하여 입력된 n번째 항과 비교
            calculated_an = a1 * (result**(n-1))
            st.markdown(f"**검증:** 계산된 공비로 구한 $n$번째 항 ($a_1 \\cdot r^{n-1}$) = **{calculated_an:.6f}**")
            
            # 부동소수점 오차를 고려한 비교 (아주 작은 오차는 허용)
            # 입력된 an과 계산된 calculated_an의 차이가 0.000001보다 작으면 동일하다고 간주
            if abs(calculated_an - an) < 1e-6:
                st.info("입력된 $n$번째 항과 계산된 $n$번째 항이 일치합니다. (미세한 오차 범위 내)")
            else:
                st.warning(f"입력된 $n$번째 항 ({an:.6f})과 계산된 $n$번째 항 ({calculated_an:.6f}) 사이에 약간의 차이가 있습니다. 이는 부동소수점 정밀도 문제일 수 있습니다.")

# 앱 하단에 추가 정보 및 공식 표시
st.markdown("---")
st.markdown("💡 등비수열 일반항: $a_n = a_1 \\cdot r^{n-1}$")
st.markdown("💡 공비 ($r$) 계산 공식: $r = (a_n / a_1)^{1/(n-1)}$")
