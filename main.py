
import os
import sys
# 경로 추가
from apps.scheduler import scheduling

sys.path.append(os.path.abspath("../../"))
if __name__ == "__main__":
    scheduling.run_schedule("16:31:00")