#!/usr/bin/env python3
"""Build the five-theme and element-module design system."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REFERENCE_COMMIT = "ba1f4175519b481cb3566616c9e5178705067904"


THEMES = [
    {
        "id": "green-white-clean", "name": "绿白清简", "order": 1, "default": True,
        "description": "绿白清简：水印刊头、轻量章节、对话引用卡与克制代码卡",
        "accent": "#01A539", "label": "TITEL", "width": "635px", "pad": "0 20px 36px",
        "source_css": "assets/source-styles/zhouxing-thin-green.css",
        "h1_watermark": "01", "h1_kicker": "SECTION TITLE",
        "font": "-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif", "body_color": "#34463B",
        "paragraph": "margin:0 0 24px!important;font-size:16px;line-height:1.95!important;letter-spacing:.035em;text-align:justify!important;",
        "h1_meta": "margin:0 0 44px;font-size:24px;font-weight:700;line-height:1.42!important;",
        "h1": "padding:10px 0 22px;border:none;border-bottom:1px solid #C8F0D2;border-radius:0;background:#FFFFFF;color:#015F25;box-shadow:none;",
        "h2_meta": "margin:54px 0 25px!important;font-size:22px;font-weight:700;line-height:1.45!important;",
        "h2": "padding:0 0 10px;border:none;border-bottom:3px solid #01A539;color:#015F25;background:#FFFFFF;",
        "label_css": "display:block;margin:0 0 6px;padding:0;background:transparent;color:#01A539;font-family:Arial,sans-serif;letter-spacing:2.5px;",
        "h3_meta": "margin:34px 0 17px!important;font-size:17px;font-weight:700;", "h3": "display:table;padding:0 0 4px;border:none;border-bottom:2px solid #C8F0D2;background:transparent;color:#015F25;",
        "quote": "padding:20px 22px;border:none;border-radius:0;background:#F2FFF5;color:#41584A;box-shadow:none;",
        "strong": "padding:0 1px;background:linear-gradient(transparent 64%,#C8F0D2 64%);color:#153D24;",
        "list": "padding-left:23px;color:#3E5145;", "li": "margin:9px 0;padding-left:4px;",
        "code": "padding:0;border:1px solid #CFE2D5;border-radius:6px;background:#F7FAF8;box-shadow:none;", "code_color": "#284734",
        "image": "border:none;border-radius:0;box-shadow:none;", "hr": "width:54px;height:3px;margin-left:auto;margin-right:auto;background:#01A539;",
        "table": "border-collapse:collapse;border-top:2px solid #01A539;border-bottom:1px solid #C8F0D2;", "th": "background:#FFFFFF;color:#015F25;border-bottom:1px solid #01A539;", "td": "background:#FFFFFF;border-bottom:1px solid #E2F3E7;",
    },
    {
        "id": "ink-blue-editorial", "name": "墨蓝刊读", "order": 2, "default": False,
        "description": "墨蓝刊读：衬线正文、通栏深色章节、居中引语与影印图片",
        "accent": "#315B7D", "label": "EDITION", "width": "677px", "pad": "0 12px 40px",
        "font": "'Songti SC',STSong,SimSun,serif", "body_color": "#263746",
        "paragraph": "margin:0 0 20px!important;font-size:16px;line-height:1.82!important;letter-spacing:.02em;text-align:left!important;",
        "h1_meta": "margin:0 0 46px;font-size:24px;font-weight:700;line-height:1.35!important;",
        "h1": "padding:12px 18px;border:none;border-top:8px solid #315B7D;border-bottom:1px solid #7895AB;border-radius:0;background:#F2F6F9;color:#132D41;box-shadow:none;text-align:center;letter-spacing:.06em;",
        "h2_meta": "margin:62px 0 28px!important;font-size:22px;font-weight:700;line-height:1.45!important;",
        "h2": "padding:18px 20px;border:none;border-radius:0;background:#183247;color:#FFFFFF;box-shadow:8px 8px 0 #DCE7EE;",
        "label_css": "display:block;margin:0 0 8px;padding:0;background:transparent;color:#AFC3D2;font-family:Georgia,serif;letter-spacing:4px;",
        "h3_meta": "margin:38px 0 18px!important;font-size:18px;font-weight:700;", "h3": "padding:0 0 9px;border:none;border-bottom:1px solid #7895AB;background:transparent;color:#183247;letter-spacing:.08em;",
        "quote": "padding:14px 20px;border:none;border-top:1px solid #7895AB;border-bottom:1px solid #7895AB;border-radius:0;background:#FFFFFF;color:#294C67;box-shadow:none;text-align:center;font-size:18px;",
        "strong": "padding:0 2px;background:linear-gradient(transparent 68%,#DCE7EE 68%);color:#183247;",
        "list": "padding:18px 24px 18px 42px;background:#F2F6F9;color:#294C67;", "li": "margin:8px 0;padding-left:5px;",
        "code": "padding:0;border:none;border-radius:0;background:#102433;box-shadow:8px 8px 0 #DCE7EE;", "code_color": "#DDEBF3",
        "image": "border:9px solid #FFFFFF;border-radius:0;box-shadow:0 0 0 1px #AFC3D2,0 16px 32px rgba(24,50,71,.16);", "hr": "height:5px;border-top:1px solid #315B7D;border-bottom:1px solid #315B7D;background:transparent;",
        "table": "border-collapse:collapse;border:1px solid #7895AB;", "th": "background:#183247;color:#FFFFFF;border:1px solid #7895AB;", "td": "background:#FFFFFF;border:1px solid #AFC3D2;",
    },
    {
        "id": "graphite-dossier", "name": "石墨档案", "order": 3, "default": False,
        "description": "石墨档案：等宽编号、超大水印感章标、密集网格与无圆角结构",
        "accent": "#4B5563", "label": "FILE", "width": "677px", "pad": "0 14px 36px",
        "font": "-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif", "body_color": "#25282D",
        "paragraph": "margin:0 0 16px!important;font-size:15px;line-height:1.72!important;letter-spacing:.01em;text-align:left!important;",
        "h1_meta": "margin:0 0 32px;font-size:24px;font-weight:750;line-height:1.32!important;",
        "h1": "padding:20px;border:1px solid #4B5563;border-radius:0;background:#111827;color:#FFFFFF;box-shadow:none;font-family:Menlo,'PingFang SC',sans-serif;letter-spacing:.01em;",
        "h2_meta": "margin:44px 0 20px!important;font-size:21px;font-weight:750;line-height:1.35!important;",
        "h2": "padding:0 0 12px;border:none;border-bottom:1px solid #4B5563;border-radius:0;background:#FFFFFF;color:#111827;",
        "label_css": "display:block;margin:0 0 -3px;padding:0;background:transparent;color:#D1D5DB;font-family:Menlo,monospace;font-size:36px;line-height:1!important;letter-spacing:-2px;",
        "h3_meta": "margin:26px 0 13px!important;font-size:15px;font-weight:700;", "h3": "padding:9px 11px;border:1px solid #9CA3AF;border-radius:0;background:#F3F4F6;color:#111827;font-family:Menlo,'PingFang SC',sans-serif;",
        "quote": "padding:18px;border:1px solid #9CA3AF;border-radius:0;background:#F9FAFB;color:#374151;box-shadow:none;font-family:Menlo,'PingFang SC',sans-serif;",
        "strong": "padding:0 1px 2px;border-bottom:2px solid #4B5563;background:transparent;color:#111827;",
        "list": "padding:0;list-style-position:inside;color:#30343A;", "li": "margin:0;padding:9px 8px;border-bottom:1px solid #D1D5DB;font-family:Menlo,'PingFang SC',sans-serif;font-size:14px;",
        "code": "padding:0;border:1px solid #111827;border-radius:0;background:#111827;box-shadow:none;", "code_color": "#E5E7EB",
        "image": "border:1px solid #9CA3AF;border-radius:0;box-shadow:none;", "hr": "height:1px;background:#4B5563;",
        "table": "border-collapse:collapse;border:1px solid #4B5563;font-family:Menlo,'PingFang SC',sans-serif;", "th": "background:#111827;color:#FFFFFF;border:1px solid #4B5563;", "td": "background:#FFFFFF;border:1px solid #D1D5DB;",
    },
    {
        "id": "sand-gold-journal", "name": "沙金手记", "order": 4, "default": False,
        "description": "沙金手记：米黄纸张、虚线撕口、硬阴影与盖章式章节",
        "accent": "#9A6A2F", "label": "TICKET", "width": "645px", "pad": "0 22px 42px",
        "font": "'Songti SC',STSong,SimSun,serif", "body_color": "#594837",
        "paragraph": "margin:0 0 21px!important;font-size:16px;line-height:1.84!important;letter-spacing:.025em;text-align:justify!important;",
        "h1_meta": "margin:0 0 40px;font-size:24px;font-weight:700;line-height:1.4!important;",
        "h1": "padding:28px 22px;border:2px solid #4E3822;border-radius:0;background:#FFFDF8;color:#4E3822;box-shadow:7px 7px 0 #C7A675;text-align:center;",
        "h2_meta": "margin:54px 0 24px!important;font-size:21px;font-weight:700;line-height:1.42!important;",
        "h2": "padding:14px 16px;border:1px dashed #9A6A2F;border-radius:0;background:#FFFDF8;color:#4E3822;box-shadow:5px 5px 0 #E9D4AE;",
        "label_css": "display:inline-block;margin:0 10px 0 0;padding:4px 8px;border:1px solid #9A6A2F;background:#9A6A2F;color:#FFFFFF;font-family:Georgia,serif;letter-spacing:2px;",
        "h3_meta": "margin:32px 0 16px!important;font-size:17px;font-weight:700;", "h3": "display:table;padding:7px 11px;border:1px solid #9A6A2F;border-radius:999px;background:#FFFDF8;color:#6B4A26;",
        "quote": "padding:22px;border:1px dashed #9A6A2F;border-radius:0;background:#FFFDF8;color:#6A5138;box-shadow:5px 5px 0 #EFE2CB;",
        "strong": "padding:1px 5px;border:1px solid #9A6A2F;border-radius:999px;background:#FFFDF8;color:#6B4A26;",
        "list": "padding:4px 16px 4px 34px;border-top:1px dashed #C7A675;border-bottom:1px dashed #C7A675;color:#594837;", "li": "margin:10px 0;padding-left:5px;",
        "code": "padding:0;border:1px dashed #9A6A2F;border-radius:0;background:#FFFDF8;box-shadow:5px 5px 0 #EFE2CB;", "code_color": "#594837",
        "image": "border:10px solid #FFFDF8;border-radius:0;box-shadow:0 0 0 1px #C7A675,8px 8px 0 #E9D4AE;", "hr": "height:0;border-top:2px dashed #9A6A2F;background:transparent;",
        "table": "border-collapse:separate;border-spacing:3px;background:#C7A675;", "th": "background:#6B4A26;color:#FFFFFF;", "td": "background:#FFFDF8;border:none;",
    },
    {
        "id": "mist-purple-story", "name": "雾紫叙事", "order": 5, "default": False,
        "description": "雾紫叙事：窄栏衬线、大段呼吸、居中章名与大字金句",
        "accent": "#7559A6", "label": "STORY", "width": "590px", "pad": "8px 28px 54px",
        "font": "'Songti SC',STSong,SimSun,serif", "body_color": "#4C4556",
        "paragraph": "margin:0 0 30px!important;font-size:16px;line-height:2.08!important;letter-spacing:.045em;text-align:justify!important;",
        "h1_meta": "margin:0 0 64px;font-size:24px;font-weight:600;line-height:1.55!important;",
        "h1": "padding:14px 8px;border:none;border-top:1px solid #DCCFF0;border-bottom:1px solid #DCCFF0;border-radius:0;background:#FFFFFF;color:#3E3158;box-shadow:none;text-align:center;letter-spacing:.1em;",
        "h2_meta": "margin:76px 0 34px!important;font-size:22px;font-weight:600;line-height:1.55!important;",
        "h2": "padding:20px 0;border:none;border-radius:0;background:#FFFFFF;color:#4E3C70;text-align:center;",
        "label_css": "display:block;margin:0 0 8px;padding:0;background:transparent;color:#A995C8;font-family:Georgia,serif;letter-spacing:5px;",
        "h3_meta": "margin:45px 0 22px!important;font-size:17px;font-weight:600;", "h3": "padding:0;border:none;background:transparent;color:#4E3C70;text-align:center;letter-spacing:.12em;",
        "quote": "padding:14px 12px;border:none;border-top:1px solid #DCCFF0;border-bottom:1px solid #DCCFF0;border-radius:0;background:#FFFFFF;color:#594A70;box-shadow:none;text-align:center;font-size:19px;line-height:2;",
        "strong": "padding:0 2px;background:linear-gradient(transparent 66%,#DCCFF0 66%);color:#3E3158;",
        "list": "padding:0;list-style-position:inside;color:#594F66;text-align:center;", "li": "margin:13px 0;padding:0;",
        "code": "padding:0;border:none;border-radius:0;background:#F4EEFC;box-shadow:none;", "code_color": "#4E3C70",
        "image": "border:none;border-radius:0;box-shadow:none;", "hr": "width:38px;height:1px;margin-left:auto;margin-right:auto;background:#7559A6;",
        "table": "border-collapse:collapse;border-top:1px solid #7559A6;border-bottom:1px solid #7559A6;", "th": "background:#FFFFFF;color:#4E3C70;border-bottom:1px solid #DCCFF0;", "td": "background:#FFFFFF;border-bottom:1px solid #EEE8F6;",
    },
]


COMPONENTS = {
    "version": 3,
    "research": {
        "source": "https://github.com/isjiamu/gzh-design-skill",
        "source_commit": REFERENCE_COMMIT,
        "borrowed_methods": ["semantic component families", "multiple variants per content role", "theme color roles", "paste-safe static CSS"],
        "not_copied": ["theme names", "component markup", "CSS declarations", "complete visual structures"],
    },
    "modules": {
        "h1": {"label": "H1 主标题", "options": [
            {"id": "theme", "label": "跟随主题", "css": ""},
            {"id": "editorial", "label": "刊头双线", "css": ".note-to-mp h1{padding:14px 8px!important;border:none!important;border-top:5px solid {{accent}}!important;border-bottom:1px solid {{soft}}!important;border-radius:0!important;background:#fff!important;color:{{dark}}!important;box-shadow:none!important;}"},
            {"id": "center-rule", "label": "居中细线", "css": ".note-to-mp h1{padding:12px 8px!important;border:none!important;border-top:1px solid {{accent}}!important;border-bottom:1px solid {{accent}}!important;border-radius:0!important;background:#fff!important;color:{{dark}}!important;box-shadow:none!important;text-align:center!important;}"}
        ]},
        "h2": {"label": "H2 章节标题", "options": [
            {"id": "theme", "label": "跟随主题", "css": ""},
            {"id": "bottom-rule", "label": "编号底线", "css": ".note-to-mp h2{padding:3px 0 10px!important;border:none!important;border-bottom:2px solid {{soft}}!important;border-radius:0!important;background:transparent!important;color:{{dark}}!important;box-shadow:none!important;}.note-to-mp h2::before{content:'SECTION TITLE';display:block!important;margin:0 0 3px!important;color:{{accent}}!important;font-size:9px!important;font-weight:650!important;line-height:1.2!important;letter-spacing:2px!important;}.note-to-mp h2 .wechatpb-heading-label{display:inline-block!important;margin:0 9px 0 0!important;padding:2px 7px!important;border-radius:3px!important;background:{{accent}}!important;color:#fff!important;}"},
            {"id": "outline-tab", "label": "描边页签", "css": ".note-to-mp h2{padding:0 0 8px!important;border:none!important;border-radius:0!important;background:#fff!important;color:{{dark}}!important;}.note-to-mp h2 .wechatpb-heading-label{display:inline-block!important;margin:0 9px 0 0!important;padding:2px 7px!important;border:1px solid {{accent}}!important;border-radius:3px!important;background:#fff!important;color:{{accent}}!important;}.note-to-mp h2::after{content:'';display:block!important;width:88px!important;height:2px!important;margin:7px 0 0!important;background:{{accent}}!important;}"}
        ]},
        "h3": {"label": "H3 小标题", "options": [
            {"id": "theme", "label": "跟随主题", "css": ""},
            {"id": "pale-pill", "label": "浅色胶囊", "css": ".note-to-mp h3{display:table!important;padding:8px 14px!important;border:none!important;border-radius:999px!important;background:{{pale}}!important;color:{{dark}}!important;}"},
            {"id": "marker-line", "label": "荧光底线", "css": ".note-to-mp h3{display:table!important;padding:0 2px 3px!important;border:none!important;border-radius:0!important;background:linear-gradient(transparent 48%,{{soft}} 48% 88%,transparent 88%)!important;color:{{dark}}!important;}"},
            {"id": "quiet-box", "label": "轻量方框", "css": ".note-to-mp h3{padding:9px 12px!important;border:1px solid {{soft}}!important;border-radius:4px!important;background:#fff!important;color:{{dark}}!important;}"}
        ]},
        "quote": {"label": "引用块", "options": [
            {"id": "theme", "label": "跟随主题", "css": ""},
            {"id": "soft-card", "label": "浅色卡片", "css": ".note-to-mp blockquote{padding:20px!important;border:1px solid {{soft}}!important;border-radius:14px!important;background:{{pale}}!important;box-shadow:0 9px 24px {{shadow}}!important;text-align:left!important;}"},
            {"id": "centered-rule", "label": "居中金句", "css": ".note-to-mp blockquote{padding:14px 16px!important;border:none!important;border-top:1px solid {{accent}}!important;border-bottom:1px solid {{accent}}!important;border-radius:0!important;background:#fff!important;box-shadow:none!important;text-align:center!important;}.note-to-mp blockquote p{text-align:center!important;font-family:'Songti SC',STSong,serif!important;}"},
            {"id": "corner-note", "label": "折角便签", "css": ".note-to-mp blockquote{padding:20px 22px!important;border:1px solid {{soft}}!important;border-radius:3px 15px 3px 15px!important;background:#fff!important;box-shadow:6px 6px 0 {{pale}}!important;text-align:left!important;}"},
            {"id": "side-accent", "label": "侧边强调", "css": ".note-to-mp blockquote{padding:18px 20px!important;border:none!important;border-left:4px solid {{accent}}!important;border-radius:0 10px 10px 0!important;background:{{pale}}!important;box-shadow:none!important;text-align:left!important;}"}
        ]},
        "code": {"label": "代码块", "options": [
            {"id": "theme", "label": "跟随主题", "css": ""},
            {"id": "dark-window", "label": "深色窗口", "css": ".note-to-mp .code-section{padding:0!important;border:1px solid {{dark}}!important;border-top:5px solid {{accent}}!important;border-radius:10px!important;background:#111827!important;box-shadow:0 12px 28px rgba(15,23,42,.16)!important;}.note-to-mp .code-section code{color:#E5E7EB!important;background:transparent!important;}"},
            {"id": "light-paper", "label": "浅色纸张", "css": ".note-to-mp .code-section{padding:0!important;border:1px solid {{soft}}!important;border-radius:8px!important;background:#F8FAFC!important;box-shadow:none!important;}.note-to-mp .code-section code{color:#334155!important;background:transparent!important;}"},
            {"id": "hard-shadow", "label": "硬边阴影", "css": ".note-to-mp .code-section{padding:0!important;border:1px solid {{accent}}!important;border-radius:3px!important;background:#fff!important;box-shadow:7px 7px 0 {{soft}}!important;}.note-to-mp .code-section code{color:{{dark}}!important;background:transparent!important;}"}
        ]},
        "strong": {"label": "加粗", "options": [
            {"id": "theme", "label": "跟随主题", "css": ""},
            {"id": "marker", "label": "荧光笔", "css": ".note-to-mp strong{padding:0 2px!important;border-radius:0!important;background:linear-gradient(transparent 60%,{{soft}} 60%)!important;color:#111827!important;}"},
            {"id": "accent", "label": "主色强调", "css": ".note-to-mp strong{padding:0!important;background:transparent!important;color:{{accent}}!important;}"},
            {"id": "soft-label", "label": "浅色标签", "css": ".note-to-mp strong{padding:2px 6px!important;border-radius:5px!important;background:{{pale}}!important;color:{{dark}}!important;}"},
            {"id": "underline", "label": "粗底线", "css": ".note-to-mp strong{padding:0 1px 2px!important;border-bottom:2px solid {{accent}}!important;background:transparent!important;color:#111827!important;}"}
        ]},
        "em": {"label": "斜体", "options": [
            {"id": "theme", "label": "跟随主题", "css": ""},
            {"id": "accent", "label": "主色斜体", "css": ".note-to-mp em{padding:0!important;background:transparent!important;color:{{accent}}!important;font-style:italic!important;}"},
            {"id": "serif", "label": "衬线旁注", "css": ".note-to-mp em{padding:0 3px!important;background:transparent!important;color:{{dark}}!important;font-family:'Songti SC',STSong,serif!important;font-style:italic!important;}"},
            {"id": "soft-underline", "label": "浅色下划线", "css": ".note-to-mp em{padding:0 1px 2px!important;border-bottom:2px solid {{soft}}!important;background:transparent!important;color:{{dark}}!important;font-style:normal!important;}"}
        ]}
    }
}

# Rich semantic variants inspired by the reference repository's component breadth,
# while keeping Zhouxing names, CSS, color roles, and structures original.
COMPONENTS["modules"]["h1"]["options"].extend([
    {"id": "dark-cover", "label": "深色封面", "css": ".note-to-mp h1{padding:15px 24px!important;border:none!important;border-radius:16px!important;background:{{dark}}!important;color:#fff!important;box-shadow:0 14px 32px {{shadow}}!important;text-align:left!important;}"},
    {"id": "ticket-cover", "label": "票据刊头", "css": ".note-to-mp h1{padding:13px 22px!important;border:1px dashed {{accent}}!important;border-radius:4px!important;background:{{pale}}!important;color:{{dark}}!important;box-shadow:7px 7px 0 {{soft}}!important;text-align:left!important;}"},
    {"id": "serif-opening", "label": "衬线开篇", "css": ".note-to-mp h1{padding:15px 12px!important;border:none!important;border-bottom:4px double {{accent}}!important;border-radius:0!important;background:#fff!important;color:{{dark}}!important;box-shadow:none!important;font-family:'Songti SC',STSong,serif!important;text-align:center!important;}"},
])
COMPONENTS["modules"]["h2"]["options"].extend([
    {"id": "watermark", "label": "水印编号", "css": ".note-to-mp h2{padding:0 0 13px!important;border:none!important;border-bottom:1px solid {{soft}}!important;border-radius:0!important;background:#fff!important;color:{{dark}}!important;}.note-to-mp h2 .wechatpb-heading-label{display:block!important;margin:0 0 -5px!important;padding:0!important;background:transparent!important;color:{{soft}}!important;font-size:34px!important;font-family:Georgia,serif!important;letter-spacing:0!important;line-height:1!important;}"},
    {"id": "centered-editorial", "label": "居中栏目", "css": ".note-to-mp h2{padding:10px 8px!important;border:none!important;border-top:1px solid {{soft}}!important;border-bottom:1px solid {{soft}}!important;border-radius:0!important;background:#fff!important;color:{{dark}}!important;text-align:center!important;}.note-to-mp h2 .wechatpb-heading-label{display:block!important;margin:0 0 5px!important;padding:0!important;background:transparent!important;color:{{accent}}!important;letter-spacing:3px!important;}"},
    {"id": "chapter-shortline", "label": "章节短线", "css": ".note-to-mp h2{padding:0 0 17px!important;border:none!important;border-radius:0!important;background:#fff!important;color:{{dark}}!important;box-shadow:none!important;font-family:'Songti SC',STSong,serif!important;text-align:left!important;}.note-to-mp h2 .wechatpb-heading-label{display:block!important;margin:0 0 8px!important;padding:0!important;background:transparent!important;color:{{accent}}!important;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC',sans-serif!important;font-size:10px!important;font-weight:700!important;letter-spacing:4px!important;}.note-to-mp h2::after{content:'';display:block!important;width:76px!important;height:3px!important;margin:15px 0 0!important;background:{{accent}}!important;}"},
])
COMPONENTS["modules"]["h3"]["options"].extend([
    {"id": "dark-pill", "label": "深色标签", "css": ".note-to-mp h3{display:table!important;padding:7px 13px!important;border:none!important;border-radius:6px!important;background:{{dark}}!important;color:#fff!important;box-shadow:4px 4px 0 {{soft}}!important;}"},
    {"id": "ticket-label", "label": "票据标签", "css": ".note-to-mp h3{display:table!important;padding:8px 12px!important;border:1px dashed {{accent}}!important;border-radius:2px!important;background:{{pale}}!important;color:{{dark}}!important;}"},
    {"id": "dot-pill", "label": "圆点胶囊", "css": ".note-to-mp h3{display:table!important;padding:8px 16px 8px 14px!important;border:1px solid {{soft}}!important;border-radius:999px!important;background:{{pale}}!important;color:{{dark}}!important;box-shadow:0 1px 3px {{shadow}}!important;}.note-to-mp h3::before{content:'';display:inline-block!important;width:8px!important;height:8px!important;margin:0 11px 1px 0!important;border-radius:50%!important;background:{{accent}}!important;}"},
])
COMPONENTS["modules"]["quote"]["options"].extend([
    {"id": "dark-summary", "label": "深色摘要", "css": ".note-to-mp blockquote{padding:22px!important;border:none!important;border-radius:12px!important;background:{{dark}}!important;color:#fff!important;box-shadow:0 12px 28px {{shadow}}!important;text-align:left!important;}.note-to-mp blockquote p{color:#fff!important;}"},
    {"id": "ticket-note", "label": "票据摘录", "css": ".note-to-mp blockquote{padding:21px!important;border:1px dashed {{accent}}!important;border-radius:3px!important;background:{{pale}}!important;color:{{dark}}!important;box-shadow:6px 6px 0 {{soft}}!important;text-align:left!important;}"},
    {"id": "serif-pullquote", "label": "衬线大引语", "css": ".note-to-mp blockquote{padding:16px 18px!important;border:none!important;border-top:4px double {{accent}}!important;border-bottom:4px double {{accent}}!important;border-radius:0!important;background:#fff!important;color:{{dark}}!important;box-shadow:none!important;text-align:center!important;}.note-to-mp blockquote p{font-family:'Songti SC',STSong,serif!important;font-size:18px!important;line-height:1.8!important;text-align:center!important;}"},
    {"id": "speech-card", "label": "对话卡片", "css": ".note-to-mp blockquote{padding:20px 22px!important;border:1px solid {{soft}}!important;border-radius:18px 18px 18px 4px!important;background:#fff!important;color:{{dark}}!important;box-shadow:0 3px 8px {{shadow}}!important;text-align:left!important;}"},
])
COMPONENTS["modules"]["code"]["options"].extend([
    {"id": "terminal-dots", "label": "终端窗口", "css": ".note-to-mp .code-section{padding:0!important;border:1px solid #111827!important;border-radius:10px!important;background:#0B1220!important;box-shadow:0 14px 30px rgba(15,23,42,.18)!important;}.note-to-mp .code-section pre{padding-top:42px!important;background-color:#0B1220!important;background-image:radial-gradient(circle at 17px 15px,#FB7185 0 4px,transparent 5px),radial-gradient(circle at 33px 15px,#FBBF24 0 4px,transparent 5px),radial-gradient(circle at 49px 15px,#34D399 0 4px,transparent 5px)!important;background-repeat:no-repeat!important;}.note-to-mp .code-section code{color:#DCE7F3!important;background:transparent!important;}"},
    {"id": "notebook", "label": "笔记纸张", "css": ".note-to-mp .code-section{padding:0!important;border:1px solid {{soft}}!important;border-radius:4px!important;background:repeating-linear-gradient(0deg,#fff 0 27px,{{pale}} 27px 28px)!important;box-shadow:5px 5px 0 {{soft}}!important;}.note-to-mp .code-section code{color:{{dark}}!important;background:transparent!important;line-height:28px!important;}"},
    {"id": "ticket-code", "label": "票据代码", "css": ".note-to-mp .code-section{padding:0!important;border:1px dashed {{accent}}!important;border-radius:3px!important;background:{{pale}}!important;box-shadow:none!important;}.note-to-mp .code-section code{color:{{dark}}!important;background:transparent!important;}"},
])
COMPONENTS["modules"]["strong"]["options"].extend([
    {"id": "dark-chip", "label": "深色标签", "css": ".note-to-mp strong{padding:2px 7px!important;border-radius:4px!important;background:{{dark}}!important;color:#fff!important;}"},
    {"id": "outline-chip", "label": "描边概念", "css": ".note-to-mp strong{padding:1px 6px!important;border:1px solid {{accent}}!important;border-radius:4px!important;background:#fff!important;color:{{dark}}!important;}"},
])
COMPONENTS["modules"]["em"]["options"].extend([
    {"id": "soft-pill", "label": "轻柔旁注", "css": ".note-to-mp em{padding:2px 7px!important;border-radius:999px!important;background:{{pale}}!important;color:{{dark}}!important;font-style:normal!important;}"},
    {"id": "hand-note", "label": "手记强调", "css": ".note-to-mp em{padding:0 3px 2px!important;border-bottom:1px dashed {{accent}}!important;background:transparent!important;color:{{accent}}!important;font-family:'Kaiti SC',STKaiti,KaiTi,serif!important;font-style:normal!important;}"},
])
COMPONENTS["modules"].update({
    "inline-code": {"label": "行内代码", "options": [
        {"id": "theme", "label": "跟随主题", "css": ""},
        {"id": "neutral-chip", "label": "灰色代码片", "css": ".note-to-mp p code,.note-to-mp li code,.note-to-mp td code{padding:2px 6px!important;border:1px solid #E2E8F0!important;border-radius:4px!important;background:#F1F5F9!important;color:#334155!important;box-shadow:none!important;}"},
        {"id": "accent-chip", "label": "主色代码片", "css": ".note-to-mp p code,.note-to-mp li code,.note-to-mp td code{padding:2px 7px!important;border:none!important;border-radius:5px!important;background:{{pale}}!important;color:{{dark}}!important;box-shadow:none!important;}"},
        {"id": "keyboard", "label": "键帽样式", "css": ".note-to-mp p code,.note-to-mp li code,.note-to-mp td code{padding:2px 7px!important;border:1px solid {{soft}}!important;border-bottom:3px solid {{accent}}!important;border-radius:5px!important;background:#fff!important;color:{{dark}}!important;box-shadow:none!important;}"},
        {"id": "dark-chip", "label": "深色代码片", "css": ".note-to-mp p code,.note-to-mp li code,.note-to-mp td code{padding:2px 7px!important;border:none!important;border-radius:4px!important;background:{{dark}}!important;color:#fff!important;box-shadow:none!important;}"},
    ]},
    "ordered-list": {"label": "有序列表", "options": [
        {"id": "theme", "label": "跟随主题", "css": ""},
        {"id": "decimal", "label": "标准数字", "css": ".note-to-mp ol{padding-left:28px!important;list-style-type:decimal!important;list-style-position:outside!important;background:transparent!important;}.note-to-mp ol li{margin:8px 0!important;padding:0 0 0 4px!important;border:none!important;background:transparent!important;}.note-to-mp ol li::marker{color:{{accent}}!important;font-weight:700!important;}"},
        {"id": "leading-zero", "label": "双位编号", "css": ".note-to-mp ol{padding-left:34px!important;list-style-type:decimal-leading-zero!important;list-style-position:outside!important;background:transparent!important;}.note-to-mp ol li{margin:9px 0!important;padding:0 0 0 5px!important;border:none!important;background:transparent!important;}.note-to-mp ol li::marker{color:{{accent}}!important;font-weight:700!important;font-variant-numeric:tabular-nums!important;}"},
        {"id": "roman", "label": "罗马编号", "css": ".note-to-mp ol{padding-left:36px!important;list-style-type:upper-roman!important;list-style-position:outside!important;background:transparent!important;}.note-to-mp ol li{margin:9px 0!important;padding:0 0 0 5px!important;border:none!important;background:transparent!important;}.note-to-mp ol li::marker{color:{{accent}}!important;font-family:Georgia,serif!important;font-weight:700!important;}"},
        {"id": "number-cards", "label": "编号卡片", "css": ".note-to-mp ol{padding-left:0!important;list-style-position:inside!important;list-style-type:decimal!important;background:transparent!important;}.note-to-mp ol li{margin:8px 0!important;padding:10px 13px!important;border:1px solid {{soft}}!important;border-radius:8px!important;background:{{pale}}!important;}.note-to-mp ol li::marker{color:{{accent}}!important;font-weight:800!important;}"},
        {"id": "rounded-number", "label": "圆角编号框", "css": ".note-to-mp ol{padding-left:0!important;list-style:none!important;background:transparent!important;}.note-to-mp ol li{margin:9px 0!important;padding:0!important;border:none!important;background:transparent!important;list-style:none!important;}.note-to-mp ol li .wechatpb-list-marker{display:inline-block!important;min-width:28px!important;margin:0 9px 0 0!important;padding:2px 7px!important;box-sizing:border-box!important;border:1px solid {{accent}}!important;border-radius:7px!important;background:{{pale}}!important;color:{{dark}}!important;font-size:12px!important;font-weight:750!important;line-height:1.5!important;text-align:center!important;vertical-align:middle!important;}"},
        {"id": "circle-number", "label": "圆形编号", "css": ".note-to-mp ol{padding-left:0!important;list-style:none!important;background:transparent!important;}.note-to-mp ol li{margin:9px 0!important;padding:0!important;border:none!important;background:transparent!important;list-style:none!important;}.note-to-mp ol li .wechatpb-list-marker{display:inline-block!important;width:26px!important;height:26px!important;margin:0 9px 0 0!important;padding:0!important;box-sizing:border-box!important;border:none!important;border-radius:50%!important;background:{{accent}}!important;color:#fff!important;font-size:12px!important;font-weight:750!important;line-height:26px!important;text-align:center!important;vertical-align:middle!important;}"},
    ]},
    "unordered-list": {"label": "无序列表", "options": [
        {"id": "theme", "label": "跟随主题", "css": ""},
        {"id": "solid-dot", "label": "实心圆点", "css": ".note-to-mp ul{padding-left:25px!important;list-style-type:disc!important;list-style-position:outside!important;background:transparent!important;}.note-to-mp ul li{margin:8px 0!important;padding:0 0 0 4px!important;border:none!important;background:transparent!important;}.note-to-mp ul li::marker{color:{{accent}}!important;}"},
        {"id": "hollow-dot", "label": "空心圆点", "css": ".note-to-mp ul{padding-left:25px!important;list-style-type:circle!important;list-style-position:outside!important;background:transparent!important;}.note-to-mp ul li{margin:8px 0!important;padding:0 0 0 4px!important;border:none!important;background:transparent!important;}.note-to-mp ul li::marker{color:{{accent}}!important;}"},
        {"id": "square", "label": "方形符号", "css": ".note-to-mp ul{padding-left:25px!important;list-style-type:square!important;list-style-position:outside!important;background:transparent!important;}.note-to-mp ul li{margin:8px 0!important;padding:0 0 0 4px!important;border:none!important;background:transparent!important;}.note-to-mp ul li::marker{color:{{accent}}!important;}"},
        {"id": "separated", "label": "细线分项", "css": ".note-to-mp ul{padding-left:0!important;list-style-position:inside!important;list-style-type:disc!important;background:transparent!important;}.note-to-mp ul li{margin:0!important;padding:11px 4px!important;border:none!important;border-bottom:1px solid {{soft}}!important;background:#fff!important;}.note-to-mp ul li::marker{color:{{accent}}!important;}"},
        {"id": "arrow", "label": "箭头符号", "css": ".note-to-mp ul{padding-left:0!important;list-style:none!important;background:transparent!important;}.note-to-mp ul li{margin:8px 0!important;padding:0!important;border:none!important;background:transparent!important;list-style:none!important;}.note-to-mp ul li .wechatpb-list-marker{display:inline-block!important;min-width:22px!important;margin:0 6px 0 0!important;color:{{accent}}!important;font-size:16px!important;font-weight:750!important;line-height:1.5!important;vertical-align:middle!important;}"},
        {"id": "soft-check", "label": "圆角对勾", "css": ".note-to-mp ul{padding-left:0!important;list-style:none!important;background:transparent!important;}.note-to-mp ul li{margin:8px 0!important;padding:0!important;border:none!important;background:transparent!important;list-style:none!important;}.note-to-mp ul li .wechatpb-list-marker{display:inline-block!important;min-width:24px!important;margin:0 8px 0 0!important;padding:1px 6px!important;box-sizing:border-box!important;border-radius:999px!important;background:{{pale}}!important;color:{{accent}}!important;font-size:12px!important;font-weight:800!important;line-height:1.6!important;text-align:center!important;vertical-align:middle!important;}"},
    ]},
    "table": {"label": "表格", "options": [
        {"id": "theme", "label": "跟随主题", "css": ""},
        {"id": "dark-header", "label": "深色表头", "css": ".note-to-mp table{width:100%!important;table-layout:fixed!important;border-collapse:collapse!important;border:1px solid {{soft}}!important;}.note-to-mp th,.note-to-mp td{box-sizing:border-box!important;padding:10px 12px!important;text-align:left!important;vertical-align:middle!important;white-space:normal!important;word-break:break-word!important;overflow-wrap:anywhere!important;}.note-to-mp th{border:1px solid {{dark}}!important;background:{{dark}}!important;color:#fff!important;}.note-to-mp td{border:1px solid {{soft}}!important;background:#fff!important;}"},
        {"id": "accent-header", "label": "主色表头", "css": ".note-to-mp table{width:100%!important;table-layout:fixed!important;border-collapse:collapse!important;border:1px solid {{soft}}!important;}.note-to-mp th,.note-to-mp td{box-sizing:border-box!important;padding:10px 12px!important;text-align:left!important;vertical-align:middle!important;white-space:normal!important;word-break:break-word!important;overflow-wrap:anywhere!important;}.note-to-mp th{border:1px solid {{accent}}!important;background:{{accent}}!important;color:#fff!important;}.note-to-mp td{border:1px solid {{soft}}!important;background:#fff!important;}"},
        {"id": "minimal-lines", "label": "极简横线", "css": ".note-to-mp table{width:100%!important;table-layout:fixed!important;border-collapse:collapse!important;border-top:2px solid {{accent}}!important;border-bottom:2px solid {{accent}}!important;}.note-to-mp th,.note-to-mp td{box-sizing:border-box!important;padding:10px 12px!important;text-align:left!important;vertical-align:middle!important;white-space:normal!important;word-break:break-word!important;overflow-wrap:anywhere!important;}.note-to-mp th{border:none!important;border-bottom:1px solid {{accent}}!important;background:#fff!important;color:{{dark}}!important;}.note-to-mp td{border:none!important;border-bottom:1px solid {{soft}}!important;background:#fff!important;}"},
        {"id": "rounded", "label": "圆角表格", "css": ".note-to-mp table{width:100%!important;table-layout:fixed!important;border-collapse:separate!important;border-spacing:0!important;border:1px solid {{soft}}!important;border-radius:12px!important;overflow:hidden!important;}.note-to-mp th,.note-to-mp td{box-sizing:border-box!important;padding:10px 12px!important;text-align:left!important;vertical-align:middle!important;white-space:normal!important;word-break:break-word!important;overflow-wrap:anywhere!important;}.note-to-mp th{border:none!important;border-bottom:1px solid {{soft}}!important;background:{{pale}}!important;color:{{dark}}!important;}.note-to-mp td{border:none!important;border-bottom:1px solid {{soft}}!important;background:#fff!important;}.note-to-mp tr:last-child td{border-bottom:none!important;}"},
    ]},
    "divider": {"label": "分隔线", "options": [
        {"id": "theme", "label": "跟随主题", "css": ""},
        {"id": "gradient", "label": "渐隐细线", "css": ".note-to-mp hr{height:1px!important;border:none!important;background:linear-gradient(to right,transparent,{{accent}},transparent)!important;}"},
        {"id": "double", "label": "编辑双线", "css": ".note-to-mp hr{height:5px!important;border:none!important;border-top:1px solid {{accent}}!important;border-bottom:1px solid {{accent}}!important;background:transparent!important;}"},
        {"id": "dashed", "label": "票据虚线", "css": ".note-to-mp hr{height:0!important;border:none!important;border-top:1px dashed {{accent}}!important;background:transparent!important;}"},
        {"id": "color-block", "label": "双色短线", "css": ".note-to-mp hr{width:96px!important;height:5px!important;margin-left:auto!important;margin-right:auto!important;border:none!important;background:linear-gradient(90deg,{{accent}} 0 58%,{{soft}} 58% 100%)!important;}"},
    ]},
    "link": {"label": "链接", "options": [
        {"id": "theme", "label": "跟随主题", "css": ""},
        {"id": "underline", "label": "主色下划线", "css": ".note-to-mp a{padding:0 1px 2px!important;border:none!important;border-bottom:1px solid {{accent}}!important;border-radius:0!important;background:transparent!important;color:{{accent}}!important;text-decoration:none!important;}"},
        {"id": "soft-pill", "label": "浅色链接", "css": ".note-to-mp a{padding:2px 7px!important;border:none!important;border-radius:999px!important;background:{{pale}}!important;color:{{dark}}!important;text-decoration:none!important;}"},
        {"id": "dotted", "label": "点线链接", "css": ".note-to-mp a{padding:0 1px 2px!important;border:none!important;border-bottom:2px dotted {{accent}}!important;border-radius:0!important;background:transparent!important;color:{{dark}}!important;text-decoration:none!important;}"},
        {"id": "dark-label", "label": "深色链接", "css": ".note-to-mp a{padding:2px 7px!important;border:none!important;border-radius:4px!important;background:{{dark}}!important;color:#fff!important;text-decoration:none!important;}"},
    ]},
})


def build_css(theme: dict, skill: Path) -> str:
    if theme.get("source_css"):
        return (skill / theme["source_css"]).read_text(encoding="utf-8")
    return f""".note-to-mp {{
  max-width:{theme['width']};margin:0 auto;padding:{theme['pad']};background:#FFFFFF;color:{theme['body_color']};
  font-family:{theme['font']};font-size:16px;line-height:1.86!important;overflow-x:hidden;word-break:break-word;
  {theme.get('container', '')}
}}
.note-to-mp p {{color:{theme['body_color']};{theme['paragraph']}}}
.note-to-mp h1 {{{theme['h1_meta']}{theme['h1']}}}
.note-to-mp h2 {{{theme['h2_meta']}{theme['h2']}}}
.note-to-mp .wechatpb-heading-label {{font-size:10px;font-weight:650;line-height:1.2!important;letter-spacing:2px;{theme['label_css']}}}
.note-to-mp h3 {{{theme['h3_meta']}line-height:1.5!important;{theme['h3']}}}
.note-to-mp h4,.note-to-mp h5,.note-to-mp h6 {{margin:28px 0 15px!important;color:{theme['body_color']};font-size:16px;font-weight:650;line-height:1.5!important;}}
.note-to-mp strong {{padding:0 2px;font-weight:700;{theme['strong']}}}
.note-to-mp em {{color:{theme['accent']};font-style:italic;}}
.note-to-mp a {{color:{theme['accent']};text-decoration:none;border-bottom:1px solid {theme['accent']};}}
.note-to-mp blockquote {{margin:0 0 26px!important;{theme['quote']}}}
.note-to-mp blockquote p {{margin:0!important;color:inherit!important;font-size:15px;line-height:1.78!important;text-align:inherit!important;}}
.note-to-mp ul,.note-to-mp ol {{margin:0 0 24px;line-height:1.82!important;{theme['list']}}}
.note-to-mp li {{{theme['li']}}}
.note-to-mp li::marker {{color:{theme['accent']};font-weight:700;}}
.note-to-mp code {{padding:2px 6px;border:1px solid #E2E8F0;border-radius:4px;background:#F1F5F9;color:#334155;font-family:Menlo,Monaco,Consolas,monospace;font-size:14px;}}
.note-to-mp .code-section {{margin:0 0 26px;overflow:hidden;{theme['code']}}}
.note-to-mp .code-section pre {{margin:0;max-height:360px;padding:17px;overflow:auto;background:transparent;white-space:pre-wrap!important;word-break:break-all!important;}}
.note-to-mp .code-section code {{display:block;padding:0;border:none;background:transparent;color:{theme['code_color']};line-height:1.65!important;}}
.note-to-mp img {{width:auto;max-width:100%;height:auto;display:block;margin:28px auto;box-sizing:border-box;{theme['image']}}}
.note-to-mp hr {{height:1px;margin:48px 0 32px;border:none;{theme['hr']}}}
.note-to-mp table {{width:100%;margin:0 0 26px;box-sizing:border-box;table-layout:fixed;font-size:14px;{theme['table']}}}
.note-to-mp th {{box-sizing:border-box;padding:10px 12px;vertical-align:middle;text-align:left;white-space:normal;word-break:break-word;overflow-wrap:anywhere;{theme['th']}}}
.note-to-mp td {{box-sizing:border-box;padding:10px 12px;vertical-align:middle;text-align:left;white-space:normal;word-break:break-word;overflow-wrap:anywhere;color:{theme['body_color']};{theme['td']}}}
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    skill = args.skill.expanduser().resolve()
    theme_dir = skill / "assets" / "style-library"
    theme_dir.mkdir(parents=True, exist_ok=True)
    generated = set()
    for theme in THEMES:
        data = {
            "id": theme["id"], "name": theme["name"], "description": theme["description"],
            "order": theme["order"], "default": theme["default"], "accent": theme["accent"],
            "hue_range": 70, "heading_label": theme["label"],
            "h1_watermark": theme.get("h1_watermark"), "h1_kicker": theme.get("h1_kicker"),
            "css": build_css(theme, skill),
            "evidence": {
                "source_type": "mixed",
                "source": "Original Zhouxing design; component-system research from isjiamu/gzh-design-skill",
                "source_commit": REFERENCE_COMMIT,
                "observed": ["semantic component grouping", "restrained color roles", "inline-style compatibility strategy"],
                "inferred": [], "unobserved": [], "confidence": "high",
            },
        }
        path = theme_dir / f"{theme['id']}.json"
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        generated.add(path.name)
    for path in theme_dir.glob("*.json"):
        if path.name not in generated:
            path.unlink()
    component_path = skill / "assets" / "component-library.json"
    component_path.write_text(json.dumps(COMPONENTS, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"themes": len(generated), "components": len(COMPONENTS["modules"]), "removed_old_themes": True}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
