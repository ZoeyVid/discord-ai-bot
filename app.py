#!/usr/bin/env python3

import os
import base64

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

bot = discord.Bot()
@bot.listen(once=True)
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Hi!"))
    print("Bot is running!")


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


@bot.command(description="Hi by ZoeyVid! (gpt-4o-mini) 0,15$/0,6$", contexts={discord.InteractionContextType.guild, discord.InteractionContextType.private_channel}, integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
async def mini(ctx, prompt: discord.Option(str, description="Der Prompt"), url: discord.Option(str, required=False, description="URL für file_search"), image: discord.Option(discord.Attachment, required=False, description="Bild"), filesearch: discord.Option(discord.Attachment, required=False, description="Datei für file_search"), codeinterpreter: discord.Option(discord.Attachment, required=False, description="Datei für code_interpreter")):
  await ctx.defer()
  print(prompt)
  print("Hi by ZoeyVid! ^(gpt-4o-mini) 0,15$/0,6$^")
  if url:
    async with async_playwright() as playwright:
      chromium = playwright.chromium
      browser = await chromium.launch()
      page = await browser.new_page(locale="de-DE", timezone_id="Europe/Berlin", user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
      await page.goto(url)
      await page.emulate_media(media="screen")
      pdf = await page.pdf(width="1440px", height="2560px", landscape=True)
      await browser.close()
      file = oaiclient.files.create(file=("website.pdf", pdf), purpose="assistants")
      assistant = oaiclient.beta.assistants.create(model="gpt-4o-mini", tools=[{"type": "file_search"}], instructions="Du befolgst die dir gegebenen Anweisungen und beachtest dabei die Webseite, welche du als PDF-Datei im Anhang findest.")
      thread = oaiclient.beta.threads.create()
      oaiclient.beta.threads.messages.create(thread.id, role="user", content=prompt, attachments=[{"file_id": file.id, "tools": [{"type": "file_search"}]}])
      run = oaiclient.beta.threads.runs.create(thread.id, assistant_id=assistant.id)
      while oaiclient.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id).status != "completed":
        pass
      all_messages = oaiclient.beta.threads.messages.list(thread_id=thread.id)
      print(all_messages.data[0].content[0].text.value)
      oaiclient.files.delete(file.id)
      oaiclient.beta.assistants.delete(assistant.id)
      oaiclient.beta.threads.delete(thread.id)
      for i in range(ceil(len(all_messages.data[0].content[0].text.value) / 4096)):
        embed = discord.Embed(title="Hi by ZoeyVid! (gpt-4o-mini) 0,15$/0,6$")
        embed.description = (all_messages.data[0].content[0].text.value[(4096*i):(4096*(i+1))])
        await ctx.respond(embed=embed)
  elif filesearch:
      filesearchfile = await filesearch.read()
      file = oaiclient.files.create(file=(filesearch.filename, filesearchfile), purpose="assistants")
      assistant = oaiclient.beta.assistants.create(model="gpt-4o-mini", tools=[{"type": "file_search"}], instructions="Du befolgst die dir gegebenen Anweisungen und beachtest dabei die Datei, welche du im Anhang findest.")
      thread = oaiclient.beta.threads.create()
      oaiclient.beta.threads.messages.create(thread.id, role="user", content=prompt, attachments=[{"file_id": file.id, "tools": [{"type": "file_search"}]}])
      run = oaiclient.beta.threads.runs.create(thread.id, assistant_id=assistant.id)
      while oaiclient.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id).status != "completed":
        pass
      all_messages = oaiclient.beta.threads.messages.list(thread_id=thread.id)
      print(all_messages.data[0].content[0].text.value)
      oaiclient.files.delete(file.id)
      oaiclient.beta.assistants.delete(assistant.id)
      oaiclient.beta.threads.delete(thread.id)
      for i in range(ceil(len(all_messages.data[0].content[0].text.value) / 4096)):
        embed = discord.Embed(title="Hi by ZoeyVid! (gpt-4o-mini) 0,15$/0,6$")
        embed.description = (all_messages.data[0].content[0].text.value[(4096*i):(4096*(i+1))])
        await ctx.respond(embed=embed)
  elif codeinterpreter:
      codeinterpreterfile = await filesearch.read()
      file = oaiclient.files.create(file=(filesearch.filename, codeinterpreterfile), purpose="assistants")
      assistant = oaiclient.beta.assistants.create(model="gpt-4o-mini", tools=[{"type": "code_interpreter"}], instructions="Du befolgst die dir gegebenen Anweisungen und beachtest dabei die Datei, welche du im Anhang findest.")
      thread = oaiclient.beta.threads.create()
      oaiclient.beta.threads.messages.create(thread.id, role="user", content=prompt, attachments=[{"file_id": file.id, "tools": [{"type": "code_interpreter"}]}])
      run = oaiclient.beta.threads.runs.create(thread.id, assistant_id=assistant.id)
      while oaiclient.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id).status != "completed":
        pass
      all_messages = oaiclient.beta.threads.messages.list(thread_id=thread.id)
      print(all_messages.data[0].content[0].text.value)
      oaiclient.files.delete(file.id)
      oaiclient.beta.assistants.delete(assistant.id)
      oaiclient.beta.threads.delete(thread.id)
      for i in range(ceil(len(all_messages.data[0].content[0].text.value) / 4096)):
        embed = discord.Embed(title="Hi by ZoeyVid! (gpt-4o-mini) 0,15$/0,6$")
        embed.description = (all_messages.data[0].content[0].text.value[(4096*i):(4096*(i+1))])
        await ctx.respond(embed=embed)
  elif image:
      imagefile = await image.read()
      file = oaiclient.files.create(file=(image.filename, imagefile), purpose="assistants")
      assistant = oaiclient.beta.assistants.create(model="gpt-4o-mini", instructions="Du befolgst die dir gegebenen Anweisungen und beachtest dabei das Bild, welche du im Anhang findest.")
      thread = oaiclient.beta.threads.create()
      oaiclient.beta.threads.messages.create(thread.id, role="user", content=[{"type": "text", "text": prompt}, {"type": "image_file", "image_file": {"file_id": file.id}}])
      run = oaiclient.beta.threads.runs.create(thread.id, assistant_id=assistant.id)
      while oaiclient.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id).status != "completed":
        pass
      all_messages = oaiclient.beta.threads.messages.list(thread_id=thread.id)
      print(all_messages.data[0].content[0].text.value)
      oaiclient.files.delete(file.id)
      oaiclient.beta.assistants.delete(assistant.id)
      oaiclient.beta.threads.delete(thread.id)
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
      page = await browser.new_page(locale="de-DE", timezone_id="Europe/Berlin", user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
      await page.goto(url)
      await page.emulate_media(media="screen")
      pdf = await page.pdf(width="1440px", height="2560px", landscape=True)
      await browser.close()
      file = oaiclient.files.create(file=("website.pdf", pdf), purpose="assistants")
      assistant = oaiclient.beta.assistants.create(model="gpt-4o", tools=[{"type": "file_search"}], instructions="Du befolgst die dir gegebenen Anweisungen und beachtest dabei die Webseite, welche du als PDF-Datei im Anhang findest.")
      thread = oaiclient.beta.threads.create()
      oaiclient.beta.threads.messages.create(thread.id, role="user", content=prompt, attachments=[{"file_id": file.id, "tools": [{"type": "file_search"}]}])
      run = oaiclient.beta.threads.runs.create(thread.id, assistant_id=assistant.id)
      while oaiclient.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id).status != "completed":
        pass
      all_messages = oaiclient.beta.threads.messages.list(thread_id=thread.id)
      print(all_messages.data[0].content[0].text.value)
      oaiclient.files.delete(file.id)
      oaiclient.beta.assistants.delete(assistant.id)
      oaiclient.beta.threads.delete(thread.id)
      for i in range(ceil(len(all_messages.data[0].content[0].text.value) / 4096)):
        embed = discord.Embed(title="Hi by ZoeyVid! (gpt-4o) 5$/15$")
        embed.description = (all_messages.data[0].content[0].text.value[(4096*i):(4096*(i+1))])
        await ctx.respond(embed=embed)
  elif filesearch:
      filesearchfile = await filesearch.read()
      file = oaiclient.files.create(file=(filesearch.filename, filesearchfile), purpose="assistants")
      assistant = oaiclient.beta.assistants.create(model="gpt-4o", tools=[{"type": "file_search"}], instructions="Du befolgst die dir gegebenen Anweisungen und beachtest dabei die Datei, welche du im Anhang findest.")
      thread = oaiclient.beta.threads.create()
      oaiclient.beta.threads.messages.create(thread.id, role="user", content=prompt, attachments=[{"file_id": file.id, "tools": [{"type": "file_search"}]}])
      run = oaiclient.beta.threads.runs.create(thread.id, assistant_id=assistant.id)
      while oaiclient.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id).status != "completed":
        pass
      all_messages = oaiclient.beta.threads.messages.list(thread_id=thread.id)
      print(all_messages.data[0].content[0].text.value)
      oaiclient.files.delete(file.id)
      oaiclient.beta.assistants.delete(assistant.id)
      oaiclient.beta.threads.delete(thread.id)
      for i in range(ceil(len(all_messages.data[0].content[0].text.value) / 4096)):
        embed = discord.Embed(title="Hi by ZoeyVid! (gpt-4o) 5$/15$")
        embed.description = (all_messages.data[0].content[0].text.value[(4096*i):(4096*(i+1))])
        await ctx.respond(embed=embed)
  elif codeinterpreter:
      codeinterpreterfile = await filesearch.read()
      file = oaiclient.files.create(file=(filesearch.filename, codeinterpreterfile), purpose="assistants")
      assistant = oaiclient.beta.assistants.create(model="gpt-4o", tools=[{"type": "code_interpreter"}], instructions="Du befolgst die dir gegebenen Anweisungen und beachtest dabei die Datei, welche du im Anhang findest.")
      thread = oaiclient.beta.threads.create()
      oaiclient.beta.threads.messages.create(thread.id, role="user", content=prompt, attachments=[{"file_id": file.id, "tools": [{"type": "code_interpreter"}]}])
      run = oaiclient.beta.threads.runs.create(thread.id, assistant_id=assistant.id)
      while oaiclient.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id).status != "completed":
        pass
      all_messages = oaiclient.beta.threads.messages.list(thread_id=thread.id)
      print(all_messages.data[0].content[0].text.value)
      oaiclient.files.delete(file.id)
      oaiclient.beta.assistants.delete(assistant.id)
      oaiclient.beta.threads.delete(thread.id)
      for i in range(ceil(len(all_messages.data[0].content[0].text.value) / 4096)):
        embed = discord.Embed(title="Hi by ZoeyVid! (gpt-4o) 5$/15$")
        embed.description = (all_messages.data[0].content[0].text.value[(4096*i):(4096*(i+1))])
        await ctx.respond(embed=embed)
  elif image:
      imagefile = await image.read()
      file = oaiclient.files.create(file=(image.filename, imagefile), purpose="assistants")
      assistant = oaiclient.beta.assistants.create(model="gpt-4o", instructions="Du befolgst die dir gegebenen Anweisungen und beachtest dabei das Bild, welche du im Anhang findest.")
      thread = oaiclient.beta.threads.create()
      oaiclient.beta.threads.messages.create(thread.id, role="user", content=[{"type": "text", "text": prompt}, {"type": "image_file", "image_file": {"file_id": file.id}}])
      run = oaiclient.beta.threads.runs.create(thread.id, assistant_id=assistant.id)
      while oaiclient.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id).status != "completed":
        pass
      all_messages = oaiclient.beta.threads.messages.list(thread_id=thread.id)
      print(all_messages.data[0].content[0].text.value)
      oaiclient.files.delete(file.id)
      oaiclient.beta.assistants.delete(assistant.id)
      oaiclient.beta.threads.delete(thread.id)
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


@bot.command(description="Hi by ZoeyVid! (claude-3-haiku) 0,25$/1,25$", contexts={discord.InteractionContextType.guild, discord.InteractionContextType.private_channel}, integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
@default_permissions(administrator=True)
async def haiku(ctx, prompt: discord.Option(str, description="Der Prompt"), jpeg: discord.Option(discord.Attachment, required=False, description="Bild"), png: discord.Option(discord.Attachment, required=False, description="Bild"), gif: discord.Option(discord.Attachment, required=False, description="Bild"), webp: discord.Option(discord.Attachment, required=False, description="Bild")):
  await ctx.defer()
  print(prompt)
  print("Hi by ZoeyVid! ^(claude-3-haiku) 0,25$/1,25$^")
  if jpeg:
    imagefile = await jpeg.read()
    message = aclient.messages.create(
      model="claude-3-haiku-20240307",
      max_tokens=4096,
      system="u befolgst die dir gegebenen Anweisungen und beachtest dabei das Bild, welche du im Anhang findest.",
      messages=[
        {"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image", "source": { "type": "base64", "media_type": "image/jpeg", "data": base64.b64encode(imagefile).decode("utf-8")}}]}]
    )
    for i in range(ceil(len(message.content[0].text) / 4096)):
      embed = discord.Embed(title="Hi by ZoeyVid! (claude-3-haiku) 0,25$/1,25$")
      embed.description = (message.content[0].text[(4096*i):(4096*(i+1))])
      await ctx.respond(embed=embed)
  elif png:
    imagefile = await png.read()
    message = aclient.messages.create(
      model="claude-3-haiku-20240307",
      max_tokens=4096,
      system="u befolgst die dir gegebenen Anweisungen und beachtest dabei das Bild, welche du im Anhang findest.",
      messages=[
        {"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image", "source": { "type": "base64", "media_type": "image/png", "data": base64.b64encode(imagefile).decode("utf-8")}}]}]
    )
    for i in range(ceil(len(message.content[0].text) / 4096)):
      embed = discord.Embed(title="Hi by ZoeyVid! (claude-3-haiku) 0,25$/1,25$")
      embed.description = (message.content[0].text[(4096*i):(4096*(i+1))])
      await ctx.respond(embed=embed)
  elif gif:
    imagefile = await gif.read()
    message = aclient.messages.create(
      model="claude-3-haiku-20240307",
      max_tokens=4096,
      system="u befolgst die dir gegebenen Anweisungen und beachtest dabei das Bild, welche du im Anhang findest.",
      messages=[
        {"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image", "source": { "type": "base64", "media_type": "image/gif", "data": base64.b64encode(imagefile).decode("utf-8")}}]}]
    )
    for i in range(ceil(len(message.content[0].text) / 4096)):
      embed = discord.Embed(title="Hi by ZoeyVid! (claude-3-haiku) 0,25$/1,25$")
      embed.description = (message.content[0].text[(4096*i):(4096*(i+1))])
      await ctx.respond(embed=embed)
  elif webp:
    imagefile = await webp.read()
    message = aclient.messages.create(
      model="claude-3-haiku-20240307",
      max_tokens=4096,
      system="u befolgst die dir gegebenen Anweisungen und beachtest dabei das Bild, welche du im Anhang findest.",
      messages=[
        {"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image", "source": { "type": "base64", "media_type": "image/webp", "data": base64.b64encode(imagefile).decode("utf-8")}}]}]
    )
    for i in range(ceil(len(message.content[0].text) / 4096)):
      embed = discord.Embed(title="Hi by ZoeyVid! (claude-3-haiku) 0,25$/1,25$")
      embed.description = (message.content[0].text[(4096*i):(4096*(i+1))])
      await ctx.respond(embed=embed)
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

    
@bot.command(description="Hi by ZoeyVid! (claude-3-5-sonnet) 3$/15$", contexts={discord.InteractionContextType.guild, discord.InteractionContextType.private_channel}, integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
@default_permissions(administrator=True)
async def sonnet(ctx, prompt: discord.Option(str, description="Der Prompt"), jpeg: discord.Option(discord.Attachment, required=False, description="Bild"), png: discord.Option(discord.Attachment, required=False, description="Bild"), gif: discord.Option(discord.Attachment, required=False, description="Bild"), webp: discord.Option(discord.Attachment, required=False, description="Bild")):
  await ctx.defer()
  print(prompt)
  print("Hi by ZoeyVid! ^(claude-3-5-sonnet) 3$/15$^")
  if jpeg:
    imagefile = await jpeg.read()
    message = aclient.messages.create(
      model="claude-3-5-sonnet-latest",
      max_tokens=4096,
      system="u befolgst die dir gegebenen Anweisungen und beachtest dabei das Bild, welche du im Anhang findest.",
      messages=[
        {"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image", "source": { "type": "base64", "media_type": "image/jpeg", "data": base64.b64encode(imagefile).decode("utf-8")}}]}]
    )
    for i in range(ceil(len(message.content[0].text) / 4096)):
      embed = discord.Embed(title="Hi by ZoeyVid! (claude-3-5-sonnet) 3$/15$")
      embed.description = (message.content[0].text[(4096*i):(4096*(i+1))])
      await ctx.respond(embed=embed)
  elif png:
    imagefile = await png.read()
    message = aclient.messages.create(
      model="claude-3-5-sonnet-latest",
      max_tokens=4096,
      system="u befolgst die dir gegebenen Anweisungen und beachtest dabei das Bild, welche du im Anhang findest.",
      messages=[
        {"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image", "source": { "type": "base64", "media_type": "image/png", "data": base64.b64encode(imagefile).decode("utf-8")}}]}]
    )
    for i in range(ceil(len(message.content[0].text) / 4096)):
      embed = discord.Embed(title="Hi by ZoeyVid! (claude-3-5-sonnet) 3$/15$")
      embed.description = (message.content[0].text[(4096*i):(4096*(i+1))])
      await ctx.respond(embed=embed)
  elif gif:
    imagefile = await gif.read()
    message = aclient.messages.create(
      model="claude-3-5-sonnet-latest",
      max_tokens=4096,
      system="u befolgst die dir gegebenen Anweisungen und beachtest dabei das Bild, welche du im Anhang findest.",
      messages=[
        {"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image", "source": { "type": "base64", "media_type": "image/gif", "data": base64.b64encode(imagefile).decode("utf-8")}}]}]
    )
    for i in range(ceil(len(message.content[0].text) / 4096)):
      embed = discord.Embed(title="Hi by ZoeyVid! (claude-3-5-sonnet) 3$/15$")
      embed.description = (message.content[0].text[(4096*i):(4096*(i+1))])
      await ctx.respond(embed=embed)
  elif webp:
    imagefile = await webp.read()
    message = aclient.messages.create(
      model="claude-3-5-sonnet-latest",
      max_tokens=4096,
      system="u befolgst die dir gegebenen Anweisungen und beachtest dabei das Bild, welche du im Anhang findest.",
      messages=[
        {"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image", "source": { "type": "base64", "media_type": "image/webp", "data": base64.b64encode(imagefile).decode("utf-8")}}]}]
    )
    for i in range(ceil(len(message.content[0].text) / 4096)):
      embed = discord.Embed(title="Hi by ZoeyVid! (claude-3-5-sonnet) 3$/15$")
      embed.description = (message.content[0].text[(4096*i):(4096*(i+1))])
      await ctx.respond(embed=embed)
  else:
    message = aclient.messages.create(
      model="claude-3-5-sonnet-latest",
      max_tokens=4096,
      system="Du befolgst die dir gegebenen Anweisungen.",
      messages=[
        {"role": "user", "content": prompt}
      ]
    )
    for i in range(ceil(len(message.content[0].text) / 4096)):
      embed = discord.Embed(title="Hi by ZoeyVid! (claude-3-5-sonnet) 3$/15$")
      embed.description = (message.content[0].text[(4096*i):(4096*(i+1))])
      await ctx.respond(embed=embed)


@bot.command(description="Hi by ZoeyVid! (claude-3-opus) 15$/75$", contexts={discord.InteractionContextType.guild, discord.InteractionContextType.private_channel}, integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
@default_permissions(administrator=True)
async def opus(ctx, prompt: discord.Option(str, description="Der Prompt"), jpeg: discord.Option(discord.Attachment, required=False, description="Bild"), png: discord.Option(discord.Attachment, required=False, description="Bild"), gif: discord.Option(discord.Attachment, required=False, description="Bild"), webp: discord.Option(discord.Attachment, required=False, description="Bild")):
  await ctx.defer()
  print(prompt)
  print("Hi by ZoeyVid! ^(claude-3-opus) 15$/75$^")
  if jpeg:
    imagefile = await jpeg.read()
    message = aclient.messages.create(
      model="claude-3-opus-latest",
      max_tokens=4096,
      system="u befolgst die dir gegebenen Anweisungen und beachtest dabei das Bild, welche du im Anhang findest.",
      messages=[
        {"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image", "source": { "type": "base64", "media_type": "image/jpeg", "data": base64.b64encode(imagefile).decode("utf-8")}}]}]
    )
    for i in range(ceil(len(message.content[0].text) / 4096)):
      embed = discord.Embed(title="Hi by ZoeyVid! (claude-3-opus) 15$/75$")
      embed.description = (message.content[0].text[(4096*i):(4096*(i+1))])
      await ctx.respond(embed=embed)
  elif png:
    imagefile = await png.read()
    message = aclient.messages.create(
      model="claude-3-opus-latest",
      max_tokens=4096,
      system="u befolgst die dir gegebenen Anweisungen und beachtest dabei das Bild, welche du im Anhang findest.",
      messages=[
        {"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image", "source": { "type": "base64", "media_type": "image/png", "data": base64.b64encode(imagefile).decode("utf-8")}}]}]
    )
    for i in range(ceil(len(message.content[0].text) / 4096)):
      embed = discord.Embed(title="Hi by ZoeyVid! (claude-3-opus) 15$/75$")
      embed.description = (message.content[0].text[(4096*i):(4096*(i+1))])
      await ctx.respond(embed=embed)
  elif gif:
    imagefile = await gif.read()
    message = aclient.messages.create(
      model="claude-3-opus-latest",
      max_tokens=4096,
      system="u befolgst die dir gegebenen Anweisungen und beachtest dabei das Bild, welche du im Anhang findest.",
      messages=[
        {"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image", "source": { "type": "base64", "media_type": "image/gif", "data": base64.b64encode(imagefile).decode("utf-8")}}]}]
    )
    for i in range(ceil(len(message.content[0].text) / 4096)):
      embed = discord.Embed(title="Hi by ZoeyVid! (claude-3-opus) 15$/75$")
      embed.description = (message.content[0].text[(4096*i):(4096*(i+1))])
      await ctx.respond(embed=embed)
  elif webp:
    imagefile = await webp.read()
    message = aclient.messages.create(
      model="claude-3-opus-latest",
      max_tokens=4096,
      system="u befolgst die dir gegebenen Anweisungen und beachtest dabei das Bild, welche du im Anhang findest.",
      messages=[
        {"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image", "source": { "type": "base64", "media_type": "image/webp", "data": base64.b64encode(imagefile).decode("utf-8")}}]}]
    )
    for i in range(ceil(len(message.content[0].text) / 4096)):
      embed = discord.Embed(title="Hi by ZoeyVid! (claude-3-opus) 15$/75$")
      embed.description = (message.content[0].text[(4096*i):(4096*(i+1))])
      await ctx.respond(embed=embed)
  else:
    message = aclient.messages.create(
      model="claude-3-opus-latest",
      max_tokens=4096,
      system="Du befolgst die dir gegebenen Anweisungen.",
      messages=[
        {"role": "user", "content": prompt}
      ]
    )
    for i in range(ceil(len(message.content[0].text) / 4096)):
      embed = discord.Embed(title="Hi by ZoeyVid! (claude-3-opus) 15$/75$")
      embed.description = (message.content[0].text[(4096*i):(4096*(i+1))])
      await ctx.respond(embed=embed)


@bot.command(description="Hi by ZoeyVid! (gflash)", contexts={discord.InteractionContextType.guild, discord.InteractionContextType.private_channel}, integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
async def gflash(ctx, prompt: discord.Option(str, description="Der Prompt")):
  await ctx.defer()
  print(prompt)
  print("Hi by ZoeyVid! ^(gflash)^")
  model = genai.GenerativeModel("gemini-1.5-flash-latest")
  response = model.generate_content(prompt)
  for i in range(ceil(len(response.text) / 4096)):
    embed = discord.Embed(title="Hi by ZoeyVid! (gflash)")
    embed.description = (response.text[(4096*i):(4096*(i+1))])
    await ctx.respond(embed=embed)


@bot.command(description="Hi by ZoeyVid! (gpro)", contexts={discord.InteractionContextType.guild, discord.InteractionContextType.private_channel}, integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
async def gpro(ctx, prompt: discord.Option(str, description="Der Prompt")):
  await ctx.defer()
  print(prompt)
  print("Hi by ZoeyVid! ^(gpro)^")
  model = genai.GenerativeModel("gemini-1.5-pro-latest")
  response = model.generate_content(prompt)
  for i in range(ceil(len(response.text) / 4096)):
    embed = discord.Embed(title="Hi by ZoeyVid! (gpro)")
    embed.description = (response.text[(4096*i):(4096*(i+1))])
    await ctx.respond(embed=embed)

bot.run(os.environ["BOT_KEY"])
