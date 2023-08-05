# -*- coding:utf-8 -*-
from django.dispatch import Signal

# ===user_course====
# 用户课程：新增/结课
# status：0-新增/1-结课
user_course_changed = Signal(providing_args=["user_course", 'status'])

# 作业被评分前发出的信号
assignment_will_be_scored = Signal(providing_args=["user_course_section", "request"])

# 作业评分后发出的信号
assignment_was_scored = Signal(providing_args=["user_course_section", "request"])

# 更新课件直播时长后发送的信号
ucs_update_time = Signal(providing_args=['user_course_section'])
# 课程通过后发送的信号
ucs_passed = Signal(providing_args=['user_course_section'])

# 直播回调后发出的信号
live_callback_finished = Signal(providing_args=["user_live", "coin_multiple"])
# 直播隐藏后发送信号
user_live_delete = Signal(providing_args=["user_live", "op_user"])
# 直播恢复后发送信号
user_live_recover = Signal(providing_args=["user_live", "op_user"])

# 笔记创建的信号
section_note_created = Signal(providing_args=["user_section_note_id"])

# 直播评论后发出的信号
user_live_comment = Signal(providing_args=['user_live', 'comment_user'])

# 认证更新后发送的信号
user_certify_update_status = Signal(providing_args=['user_certify', 'status'])