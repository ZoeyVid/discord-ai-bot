#!/usr/bin/env python3
import io
import os
import base64
import mimetypes

import discord
import anthropic
import google.generativeai as genai

from math import ceil
from openai import OpenAI
from discord import default_permissions
from playwright.async_api import async_playwright

if "OAI_KEY" in os.environ:
  oaiclient = OpenAI(api_key=os.environ["OAI_KEY"])
if "A_KEY" in os.environ:
  aclient = anthropic.Anthropic(api_key=os.environ["A_KEY"])
if "G_KEY" in os.environ:
  genai.configure(api_key=os.environ["G_KEY"])

if not "OAI_KEY" in os.environ and not "A_KEY" in os.environ and not "G_KEY" in os.environ:
  print("OAI_KEY and A_KEY and G_KEY not set")
  exit(1)

bot = discord.Bot()
@bot.listen(once=True)
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Hi!"))
    print("Bot is running!")


if "OAI_KEY" in os.environ:
  @bot.command(description="Hi by ZoeyVid! (o1-mini) 3$/12$", contexts={discord.InteractionContextType.guild, discord.InteractionContextType.private_channel}, integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
  @default_permissions(administrator=True)
  async def o1mini(ctx, prompt: discord.Option(str, description="Der Prompt")):
    await ctx.defer()
    print(prompt)
    print("Hi by ZoeyVid! ^(o1-mini) 3$/12$^")
    message = oaiclient.chat.completions.create(
      model="o1-mini",
      messages=[
        {"role": "system", "content": "Du befolgst die dir gegebenen Anweisungen."},
        {"role": "user", "content": prompt}
      ]
    )
    for i in range(ceil(len(message.choices[0].message.content) / 4096)):
      embed = discord.Embed(title="Hi by ZoeyVid! (o1-mini) 3$/12$")
      embed.description = (message.choices[0].message.content[(4096*i):(4096*(i+1))])
      await ctx.respond(embed=embed)

if "OAI_KEY" in os.environ:
  @bot.command(description="Hi by ZoeyVid! (o1-preview) 15$/60$", contexts={discord.InteractionContextType.guild, discord.InteractionContextType.private_channel}, integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
  @default_permissions(administrator=True)
  async def o1preview(ctx, prompt: discord.Option(str, description="Der Prompt")):
    await ctx.defer()
    print(prompt)
    print("Hi by ZoeyVid! ^(o1-preview) 15$/60$^")
    message = oaiclient.chat.completions.create(
      model="o1-preview",
      messages=[
        {"role": "system", "content": "Du befolgst die dir gegebenen Anweisungen."},
        {"role": "user", "content": prompt}
      ]
    )
    for i in range(ceil(len(message.choices[0].message.content) / 4096)):
      embed = discord.Embed(title="Hi by ZoeyVid! (o1-preview) 15$/60$")
      embed.description = (message.choices[0].message.content[(4096*i):(4096*(i+1))])
      await ctx.respond(embed=embed)


if "OAI_KEY" in os.environ:
  @bot.command(description="Hi by ZoeyVid! (gpt-4o-mini) 0,15$/0,6$", contexts={discord.InteractionContextType.guild, discord.InteractionContextType.private_channel}, integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
  async def mini(ctx, prompt: discord.Option(str, description="Der Prompt"), url: discord.Option(str, required=False, description="URL für file_search"), image: discord.Option(discord.Attachment, required=False, description="Bild"), filesearch: discord.Option(discord.Attachment, required=False, description="Datei für file_search"), codeinterpreter: discord.Option(discord.Attachment, required=False, description="Datei für code_interpreter")):
    await ctx.defer()
    print(prompt)
    print("Hi by ZoeyVid! ^(gpt-4o-mini) 0,15$/0,6$^")
    if url:
      async with async_playwright() as playwright:
        chromium = playwright.chromium
        browser = await chromium.launch()
        page = await browser.new_page(locale="de-DE", timezone_id="Europe/Berlin", user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0")
        await page.goto(url)
        await page.emulate_media(media="screen")
        pdf = await page.pdf(width="1440px", height="2560px", landscape=True)
        await browser.close()
        file = oaiclient.files.create(file=("Webseite.pdf", pdf), purpose="assistants")
        assistant = oaiclient.beta.assistants.create(model="gpt-4o-mini", tools=[{"type": "file_search"}], instructions="Du befolgst die dir gegebenen Anweisungen und beachtest dabei die Webseite, welche du als PDF-Datei im Anhang findest.")
        thread = oaiclient.beta.threads.create()
        oaiclient.beta.threads.messages.create(thread.id, role="user", content=prompt, attachments=[{"file_id": file.id, "tools": [{"type": "file_search"}]}])
        run = oaiclient.beta.threads.runs.create(thread.id, assistant_id=assistant.id)
        while oaiclient.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id).status != "completed":
          pass
        all_messages = oaiclient.beta.threads.messages.list(thread_id=thread.id)
        print(all_messages.data[0].content[0].text.value)
        oaiclient.files.delete(file.id)
        oaiclient.beta.threads.delete(thread.id)
        oaiclient.beta.assistants.delete(assistant.id)
        for i in range(ceil(len(all_messages.data[0].content[0].text.value) / 4096)):
          embed = discord.Embed(title="Hi by ZoeyVid! (gpt-4o-mini) 0,15$/0,6$")
          embed.description = (all_messages.data[0].content[0].text.value[(4096*i):(4096*(i+1))])
          await ctx.respond(embed=embed)
    elif filesearch:
      file = oaiclient.files.create(file=(filesearch.filename, await filesearch.read()), purpose="assistants")
      assistant = oaiclient.beta.assistants.create(model="gpt-4o-mini", tools=[{"type": "file_search"}], instructions="Du befolgst die dir gegebenen Anweisungen und beachtest dabei die Datei, welche du im Anhang findest.")
      thread = oaiclient.beta.threads.create()
      oaiclient.beta.threads.messages.create(thread.id, role="user", content=prompt, attachments=[{"file_id": file.id, "tools": [{"type": "file_search"}]}])
      run = oaiclient.beta.threads.runs.create(thread.id, assistant_id=assistant.id)
      while oaiclient.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id).status != "completed":
        pass
      all_messages = oaiclient.beta.threads.messages.list(thread_id=thread.id)
      print(all_messages.data[0].content[0].text.value)
      oaiclient.files.delete(file.id)
      oaiclient.beta.threads.delete(thread.id)
      oaiclient.beta.assistants.delete(assistant.id)
      for i in range(ceil(len(all_messages.data[0].content[0].text.value) / 4096)):
        embed = discord.Embed(title="Hi by ZoeyVid! (gpt-4o-mini) 0,15$/0,6$")
        embed.description = (all_messages.data[0].content[0].text.value[(4096*i):(4096*(i+1))])
        await ctx.respond(embed=embed)
    elif codeinterpreter:
      file = oaiclient.files.create(file=(codeinterpreter.filename, await codeinterpreter.read()), purpose="assistants")
      assistant = oaiclient.beta.assistants.create(model="gpt-4o-mini", tools=[{"type": "code_interpreter"}], instructions="Du befolgst die dir gegebenen Anweisungen und beachtest dabei die Datei, welche du im Anhang findest.")
      thread = oaiclient.beta.threads.create()
      oaiclient.beta.threads.messages.create(thread.id, role="user", content=prompt, attachments=[{"file_id": file.id, "tools": [{"type": "code_interpreter"}]}])
      run = oaiclient.beta.threads.runs.create(thread.id, assistant_id=assistant.id)
      while oaiclient.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id).status != "completed":
        pass
      all_messages = oaiclient.beta.threads.messages.list(thread_id=thread.id)
      print(all_messages.data[0].content[0].text.value)
      oaiclient.files.delete(file.id)
      oaiclient.beta.threads.delete(thread.id)
      oaiclient.beta.assistants.delete(assistant.id)
      for i in range(ceil(len(all_messages.data[0].content[0].text.value) / 4096)):
        embed = discord.Embed(title="Hi by ZoeyVid! (gpt-4o-mini) 0,15$/0,6$")
        embed.description = (all_messages.data[0].content[0].text.value[(4096*i):(4096*(i+1))])
        await ctx.respond(embed=embed)
    elif image:
      file = oaiclient.files.create(file=(image.filename, await image.read()), purpose="assistants")
      assistant = oaiclient.beta.assistants.create(model="gpt-4o-mini", instructions="Du befolgst die dir gegebenen Anweisungen und beachtest dabei das Bild, welche du im Anhang findest.")
      thread = oaiclient.beta.threads.create()
      oaiclient.beta.threads.messages.create(thread.id, role="user", content=[{"type": "text", "text": prompt}, {"type": "image_file", "image_file": {"file_id": file.id}}])
      run = oaiclient.beta.threads.runs.create(thread.id, assistant_id=assistant.id)
      while oaiclient.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id).status != "completed":
        pass
      all_messages = oaiclient.beta.threads.messages.list(thread_id=thread.id)
      print(all_messages.data[0].content[0].text.value)
      oaiclient.files.delete(file.id)
      oaiclient.beta.threads.delete(thread.id)
      oaiclient.beta.assistants.delete(assistant.id)
      for i in range(ceil(len(all_messages.data[0].content[0].text.value) / 4096)):
        embed = discord.Embed(title="Hi by ZoeyVid! (gpt-4o-mini) 0,15$/0,6$")
        embed.description = (all_messages.data[0].content[0].text.value[(4096*i):(4096*(i+1))])
        await ctx.respond(embed=embed)
    else:
      message = oaiclient.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
          {"role": "system", "content": "Du befolgst die dir gegebenen Anweisungen."},
          {"role": "user", "content": prompt}
        ]
      )
      for i in range(ceil(len(message.choices[0].message.content) / 4096)):
        embed = discord.Embed(title="Hi by ZoeyVid! (gpt-4o-mini) 0,15$/0,6$")
        embed.description = (message.choices[0].message.content[(4096*i):(4096*(i+1))])
        await ctx.respond(embed=embed)

if "OAI_KEY" in os.environ:
  @bot.command(description="Hi by ZoeyVid! (gpt-4o) 5$/15$", contexts={discord.InteractionContextType.guild, discord.InteractionContextType.private_channel}, integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
  @default_permissions(administrator=True)
  async def gpt(ctx, prompt: discord.Option(str, description="Der Prompt"), url: discord.Option(str, required=False, description="URL für file_search"), image: discord.Option(discord.Attachment, required=False, description="Bild"), filesearch: discord.Option(discord.Attachment, required=False, description="Datei für file_search"), codeinterpreter: discord.Option(discord.Attachment, required=False, description="Datei für code_interpreter")):
    await ctx.defer()
    print(prompt)
    print("Hi by ZoeyVid! ^(gpt-4o) 5$/15$^")
    if url:
      async with async_playwright() as playwright:
        chromium = playwright.chromium
        browser = await chromium.launch()
        page = await browser.new_page(locale="de-DE", timezone_id="Europe/Berlin", user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0")
        await page.goto(url)
        await page.emulate_media(media="screen")
        pdf = await page.pdf(width="1440px", height="2560px", landscape=True)
        await browser.close()
        file = oaiclient.files.create(file=("Webseite.pdf", pdf), purpose="assistants")
        assistant = oaiclient.beta.assistants.create(model="gpt-4o", tools=[{"type": "file_search"}], instructions="Du befolgst die dir gegebenen Anweisungen und beachtest dabei die Webseite, welche du als PDF-Datei im Anhang findest.")
        thread = oaiclient.beta.threads.create()
        oaiclient.beta.threads.messages.create(thread.id, role="user", content=prompt, attachments=[{"file_id": file.id, "tools": [{"type": "file_search"}]}])
        run = oaiclient.beta.threads.runs.create(thread.id, assistant_id=assistant.id)
        while oaiclient.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id).status != "completed":
          pass
        all_messages = oaiclient.beta.threads.messages.list(thread_id=thread.id)
        print(all_messages.data[0].content[0].text.value)
        oaiclient.files.delete(file.id)
        oaiclient.beta.threads.delete(thread.id)
        oaiclient.beta.assistants.delete(assistant.id)
        for i in range(ceil(len(all_messages.data[0].content[0].text.value) / 4096)):
          embed = discord.Embed(title="Hi by ZoeyVid! (gpt-4o) 5$/15$")
          embed.description = (all_messages.data[0].content[0].text.value[(4096*i):(4096*(i+1))])
          await ctx.respond(embed=embed)
    elif filesearch:
      file = oaiclient.files.create(file=(filesearch.filename, await filesearch.read()), purpose="assistants")
      assistant = oaiclient.beta.assistants.create(model="gpt-4o", tools=[{"type": "file_search"}], instructions="Du befolgst die dir gegebenen Anweisungen und beachtest dabei die Datei, welche du im Anhang findest.")
      thread = oaiclient.beta.threads.create()
      oaiclient.beta.threads.messages.create(thread.id, role="user", content=prompt, attachments=[{"file_id": file.id, "tools": [{"type": "file_search"}]}])
      run = oaiclient.beta.threads.runs.create(thread.id, assistant_id=assistant.id)
      while oaiclient.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id).status != "completed":
        pass
      all_messages = oaiclient.beta.threads.messages.list(thread_id=thread.id)
      print(all_messages.data[0].content[0].text.value)
      oaiclient.files.delete(file.id)
      oaiclient.beta.threads.delete(thread.id)
      oaiclient.beta.assistants.delete(assistant.id)
      for i in range(ceil(len(all_messages.data[0].content[0].text.value) / 4096)):
        embed = discord.Embed(title="Hi by ZoeyVid! (gpt-4o) 5$/15$")
        embed.description = (all_messages.data[0].content[0].text.value[(4096*i):(4096*(i+1))])
        await ctx.respond(embed=embed)
    elif codeinterpreter:
      file = oaiclient.files.create(file=(codeinterpreter.filename, await codeinterpreter.read()), purpose="assistants")
      assistant = oaiclient.beta.assistants.create(model="gpt-4o", tools=[{"type": "code_interpreter"}], instructions="Du befolgst die dir gegebenen Anweisungen und beachtest dabei die Datei, welche du im Anhang findest.")
      thread = oaiclient.beta.threads.create()
      oaiclient.beta.threads.messages.create(thread.id, role="user", content=prompt, attachments=[{"file_id": file.id, "tools": [{"type": "code_interpreter"}]}])
      run = oaiclient.beta.threads.runs.create(thread.id, assistant_id=assistant.id)
      while oaiclient.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id).status != "completed":
        pass
      all_messages = oaiclient.beta.threads.messages.list(thread_id=thread.id)
      print(all_messages.data[0].content[0].text.value)
      oaiclient.files.delete(file.id)
      oaiclient.beta.threads.delete(thread.id)
      oaiclient.beta.assistants.delete(assistant.id)
      for i in range(ceil(len(all_messages.data[0].content[0].text.value) / 4096)):
        embed = discord.Embed(title="Hi by ZoeyVid! (gpt-4o) 5$/15$")
        embed.description = (all_messages.data[0].content[0].text.value[(4096*i):(4096*(i+1))])
        await ctx.respond(embed=embed)
    elif image:
      file = oaiclient.files.create(file=(image.filename, await image.read()), purpose="assistants")
      assistant = oaiclient.beta.assistants.create(model="gpt-4o", instructions="Du befolgst die dir gegebenen Anweisungen und beachtest dabei das Bild, welche du im Anhang findest.")
      thread = oaiclient.beta.threads.create()
      oaiclient.beta.threads.messages.create(thread.id, role="user", content=[{"type": "text", "text": prompt}, {"type": "image_file", "image_file": {"file_id": file.id}}])
      run = oaiclient.beta.threads.runs.create(thread.id, assistant_id=assistant.id)
      while oaiclient.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id).status != "completed":
        pass
      all_messages = oaiclient.beta.threads.messages.list(thread_id=thread.id)
      print(all_messages.data[0].content[0].text.value)
      oaiclient.files.delete(file.id)
      oaiclient.beta.threads.delete(thread.id)
      oaiclient.beta.assistants.delete(assistant.id)
      for i in range(ceil(len(all_messages.data[0].content[0].text.value) / 4096)):
        embed = discord.Embed(title="Hi by ZoeyVid! (gpt-4o) 5$/15$")
        embed.description = (all_messages.data[0].content[0].text.value[(4096*i):(4096*(i+1))])
        await ctx.respond(embed=embed)
    else:
      message = oaiclient.chat.completions.create(
        model="gpt-4o",
        messages=[
          {"role": "system", "content": "Du befolgst die dir gegebenen Anweisungen."},
          {"role": "user", "content": prompt}
        ]
      )
      for i in range(ceil(len(message.choices[0].message.content) / 4096)):
        embed = discord.Embed(title="Hi by ZoeyVid! (gpt-4o) 5$/15$")
        embed.description = (message.choices[0].message.content[(4096*i):(4096*(i+1))])
        await ctx.respond(embed=embed)


if "A_KEY" in os.environ:
  @bot.command(description="Hi by ZoeyVid! (claude-3-haiku) 0,25$/1,25$", contexts={discord.InteractionContextType.guild, discord.InteractionContextType.private_channel}, integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
  @default_permissions(administrator=True)
  async def haiku3(ctx, prompt: discord.Option(str, description="Der Prompt"), image: discord.Option(discord.Attachment, required=False, description="Bild")):
    await ctx.defer()
    print(prompt)
    print("Hi by ZoeyVid! ^(claude-3-haiku) 0,25$/1,25$^")
    if image:
      if mimetypes.guess_type(image.filename)[0] == "image/jpeg" or mimetypes.guess_type(image.filename)[0] == "image/png" or mimetypes.guess_type(image.filename)[0] == "image/gif" or mimetypes.guess_type(image.filename)[0] == "image/webp":
        message = aclient.messages.create(
          model="claude-3-haiku-20240307",
          max_tokens=4096,
          system="Du befolgst die dir gegebenen Anweisungen und beachtest dabei das Bild, welche du im Anhang findest.",
          messages=[
            {"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image", "source": { "type": "base64", "media_type": mimetypes.guess_type(image.filename)[0], "data": base64.b64encode(await image.read()).decode("utf-8")}}]}]
        )
        for i in range(ceil(len(message.content[0].text) / 4096)):
          embed = discord.Embed(title="Hi by ZoeyVid! (claude-3-haiku) 0,25$/1,25$")
          embed.description = (message.content[0].text[(4096*i):(4096*(i+1))])
          await ctx.respond(embed=embed)
      else:
        await ctx.respond("Dateityp nicht unterstützt!")
    else:
      message = aclient.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=4096,
        system="Du befolgst die dir gegebenen Anweisungen.",
        messages=[
          {"role": "user", "content": prompt}
        ]
      )
      for i in range(ceil(len(message.content[0].text) / 4096)):
        embed = discord.Embed(title="Hi by ZoeyVid! (claude-3-haiku) 0,25$/1,25$")
        embed.description = (message.content[0].text[(4096*i):(4096*(i+1))])
        await ctx.respond(embed=embed)

if "A_KEY" in os.environ:
  @bot.command(description="Hi by ZoeyVid! (claude-3-5-haiku) 1$/5$", contexts={discord.InteractionContextType.guild, discord.InteractionContextType.private_channel}, integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
  @default_permissions(administrator=True)
  async def haiku35(ctx, prompt: discord.Option(str, description="Der Prompt")):
    await ctx.defer()
    print(prompt)
    print("Hi by ZoeyVid! ^(claude-3-5-haiku) 1$/5$^")
    message = aclient.messages.create(
      model="claude-3-5-haiku-latest",
      max_tokens=8192,
      system="Du befolgst die dir gegebenen Anweisungen.",
      messages=[
        {"role": "user", "content": prompt}
      ]
    )
    for i in range(ceil(len(message.content[0].text) / 4096)):
      embed = discord.Embed(title="Hi by ZoeyVid! (claude-3-5-haiku) 1$/5$")
      embed.description = (message.content[0].text[(4096*i):(4096*(i+1))])
      await ctx.respond(embed=embed)

if "A_KEY" in os.environ:
  @bot.command(description="Hi by ZoeyVid! (claude-3-5-sonnet) 3$/15$", contexts={discord.InteractionContextType.guild, discord.InteractionContextType.private_channel}, integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
  @default_permissions(administrator=True)
  async def sonnet(ctx, prompt: discord.Option(str, description="Der Prompt"), url: discord.Option(str, required=False, description="URL zum screenshoten"), file: discord.Option(discord.Attachment, required=False, description="Datei")):
    await ctx.defer()
    print(prompt)
    print("Hi by ZoeyVid! ^(claude-3-5-sonnet) 3$/15$^")
    if url:
      async with async_playwright() as playwright:
        chromium = playwright.chromium
        browser = await chromium.launch()
        page = await browser.new_page(screen={"width": 1440, "height": 2560}, locale="de-DE", timezone_id="Europe/Berlin", user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0")
        await page.goto(url)
        await page.emulate_media(media="screen")
        pdf = await page.pdf(width="1440px", height="2560px", landscape=True)
        await browser.close()
        message = aclient.messages.create(
          model="claude-3-5-sonnet-latest",
          max_tokens=8192,
          system="Du befolgst die dir gegebenen Anweisungen und beachtest dabei das Bild, welche du im Anhang findest.",
          messages=[
            {"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image", "source": { "type": "base64", "media_type": "image/png", "data": base64.b64encode(screenshot).decode("utf-8")}}]}]
        )
        for i in range(ceil(len(message.content[0].text) / 4096)):
          embed = discord.Embed(title="Hi by ZoeyVid! (claude-3-5-sonnet) 15$/75$")
          embed.description = (message.content[0].text[(4096*i):(4096*(i+1))])
          await ctx.respond(embed=embed)
    elif file:
      if mimetypes.guess_type(file.filename)[0] == "image/jpeg" or mimetypes.guess_type(file.filename)[0] == "image/png" or mimetypes.guess_type(file.filename)[0] == "image/gif" or mimetypes.guess_type(file.filename)[0] == "image/webp":
        message = aclient.messages.create(
          model="claude-3-5-sonnet-latest",
          max_tokens=8192,
          system="Du befolgst die dir gegebenen Anweisungen und beachtest dabei das Bild, welches du im Anhang findest.",
          messages=[
            {"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image", "source": { "type": "base64", "media_type": mimetypes.guess_type(file.filename)[0], "data": base64.b64encode(await file.read()).decode("utf-8")}}]}]
        )
        for i in range(ceil(len(message.content[0].text) / 4096)):
          embed = discord.Embed(title="Hi by ZoeyVid! (claude-3-5-sonnet) 3$/15$")
          embed.description = (message.content[0].text[(4096*i):(4096*(i+1))])
          await ctx.respond(embed=embed)
      elif mimetypes.guess_type(file.filename)[0] == "application/pdf":
        message = aclient.beta.messages.create(
          model="claude-3-5-sonnet-latest",
          betas=["pdfs-2024-09-25"],
          max_tokens=8192,
          system="Du befolgst die dir gegebenen Anweisungen und beachtest dabei die PDF, welche du im Anhang findest.",
          messages=[
            {"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "document", "source": { "type": "base64", "media_type": "application/pdf", "data": base64.b64encode(await file.read()).decode("utf-8")}}]}]
        )
        for i in range(ceil(len(message.content[0].text) / 4096)):
          embed = discord.Embed(title="Hi by ZoeyVid! (claude-3-5-sonnet) 3$/15$")
          embed.description = (message.content[0].text[(4096*i):(4096*(i+1))])
          await ctx.respond(embed=embed)
      else:
        await ctx.respond("Dateityp nicht unterstützt! (jpeg/png/gif/webp/pdf)")
    else:
      message = aclient.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=8192,
        system="Du befolgst die dir gegebenen Anweisungen.",
        messages=[
          {"role": "user", "content": prompt}
        ]
      )
      for i in range(ceil(len(message.content[0].text) / 4096)):
        embed = discord.Embed(title="Hi by ZoeyVid! (claude-3-5-sonnet) 3$/15$")
        embed.description = (message.content[0].text[(4096*i):(4096*(i+1))])
        await ctx.respond(embed=embed)

if "G_KEY" in os.environ:
  @bot.command(description="Hi by ZoeyVid! (gflash)", contexts={discord.InteractionContextType.guild, discord.InteractionContextType.private_channel}, integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
  async def gflash(ctx, prompt: discord.Option(str, description="Der Prompt"), url: discord.Option(str, required=False, description="URL"), file: discord.Option(discord.Attachment, required=False, description="Datei")):
    await ctx.defer()
    print(prompt)
    print("Hi by ZoeyVid! ^(gflash)^")
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    if url:
      async with async_playwright() as playwright:
        chromium = playwright.chromium
        browser = await chromium.launch()
        page = await browser.new_page(locale="de-DE", timezone_id="Europe/Berlin", user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0")
        await page.goto(url)
        await page.emulate_media(media="screen")
        pdf = await page.pdf(width="1440px", height="2560px", landscape=True)
        await browser.close()
        file = genai.upload_file(io.BytesIO(pdf), mime_type="application/pdf")
        file.delete()
        response = model.generate_content([prompt, file])
        for i in range(ceil(len(response.text) / 4096)):
          embed = discord.Embed(title="Hi by ZoeyVid! (gflash)")
          embed.description = (response.text[(4096*i):(4096*(i+1))])
          await ctx.respond(embed=embed)
    elif file:
      fileu = genai.upload_file(io.BytesIO(await file.read()), mime_type=mimetypes.guess_type(file.filename)[0])
      response = model.generate_content([prompt, fileu])
      fileu.delete()
      for i in range(ceil(len(response.text) / 4096)):
        embed = discord.Embed(title="Hi by ZoeyVid! (gflash)")
        embed.description = (response.text[(4096*i):(4096*(i+1))])
        await ctx.respond(embed=embed)
    else:
      response = model.generate_content(prompt)
      for i in range(ceil(len(response.text) / 4096)):
        embed = discord.Embed(title="Hi by ZoeyVid! (gpro)")
        embed.description = (response.text[(4096*i):(4096*(i+1))])
        await ctx.respond(embed=embed)

if "G_KEY" in os.environ:
  @bot.command(description="Hi by ZoeyVid! (gpro)", contexts={discord.InteractionContextType.guild, discord.InteractionContextType.private_channel}, integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
  async def gpro(ctx, prompt: discord.Option(str, description="Der Prompt"), url: discord.Option(str, required=False, description="URL"), file: discord.Option(discord.Attachment, required=False, description="Datei")):
    await ctx.defer()
    print(prompt)
    print("Hi by ZoeyVid! ^(gpro)^")
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    if url:
      async with async_playwright() as playwright:
        chromium = playwright.chromium
        browser = await chromium.launch()
        page = await browser.new_page(locale="de-DE", timezone_id="Europe/Berlin", user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0")
        await page.goto(url)
        await page.emulate_media(media="screen")
        pdf = await page.pdf(width="1440px", height="2560px", landscape=True)
        await browser.close()
        file = genai.upload_file(io.BytesIO(pdf), mime_type="application/pdf")
        response = model.generate_content([prompt, file])
        file.delete()
        for i in range(ceil(len(response.text) / 4096)):
          embed = discord.Embed(title="Hi by ZoeyVid! (gpro)")
          embed.description = (response.text[(4096*i):(4096*(i+1))])
          await ctx.respond(embed=embed)
    elif file:
      fileu = genai.upload_file(io.BytesIO(await file.read()), mime_type=mimetypes.guess_type(file.filename)[0])
      response = model.generate_content([prompt, fileu])
      fileu.delete()
      for i in range(ceil(len(response.text) / 4096)):
        embed = discord.Embed(title="Hi by ZoeyVid! (gpro)")
        embed.description = (response.text[(4096*i):(4096*(i+1))])
        await ctx.respond(embed=embed)
    else:
      response = model.generate_content(prompt)
      for i in range(ceil(len(response.text) / 4096)):
        embed = discord.Embed(title="Hi by ZoeyVid! (gpro)")
        embed.description = (response.text[(4096*i):(4096*(i+1))])
        await ctx.respond(embed=embed)


if "BOT_KEY" in os.environ:
  bot.run(os.environ["BOT_KEY"])
else:
  print("Bot key is missing")
  exit(1)
