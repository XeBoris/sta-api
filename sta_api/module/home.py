from flask import Blueprint, redirect, request
main_routes = Blueprint('main_routes', __name__,)

@main_routes.route('/')
def home():
    return "Welcome to strava-main"
