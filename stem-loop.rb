#!/usr/bin/env ruby
# encoding: utf-8

require 'rubygems'
require 'bundler/setup'

Bundler.require(:default)

require 'fileutils' # Necessary?

include ActionView::Helpers::DateHelper

require './lib/infernal'
require './lib/rfam'
