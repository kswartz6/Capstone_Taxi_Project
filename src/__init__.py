import os
import sys
import logging
import json
import pymongo
from flask import Flask, Response, render_template, request, redirect, url_for, send_from_directory, g, session
import controller.query