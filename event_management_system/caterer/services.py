from flask import render_template, redirect, url_for, request

from event_management_system.book_event.models import Event
from event_management_system.caterer.forms import CatererAddCategoryForm
from event_management_system.caterer.models import Caterer, CatererGetFoodCategory, FoodCategory
from event_management_system.venue.models import Venues, VenueGetCaterer


class CatererClass:
    def get_event(self):
        """
        get all the events where the caterer has served or is going to serve the food
        :return: caterer_check_events template
        """
        caterer = Caterer.get_current_caterer()
        event_detail = Event.event_detail_for_caterer(caterer_id=caterer.id)
        return render_template('caterer_check_events.html', event_detail=event_detail)

    def get_venues(self):
        """
        caterer requests venues to get business deal
        :return:caterer_venues template
        """
        get_venues_for_caterer = Venues.get_all_venues()
        current_caterer = Caterer.get_current_caterer()
        venue_get_caterer_obj_true = VenueGetCaterer.venue_get_caterer_obj_for_caterer(caterer_id=current_caterer.id,
                                                                                       is_approved_caterer=True)
        venue_get_caterer_obj_false = VenueGetCaterer.venue_get_caterer_obj_for_caterer(caterer_id=current_caterer.id,
                                                                                        is_approved_caterer=False)
        venue_get_caterer_obj_none = VenueGetCaterer.venue_get_caterer_obj_for_caterer(caterer_id=current_caterer.id,
                                                                                       is_approved_caterer=None)
        venue_get_caterer_obj_true_list = [i[0] for i in venue_get_caterer_obj_true]
        venue_get_caterer_obj_false_list = [i[0] for i in venue_get_caterer_obj_false]
        venue_get_caterer_obj_none_list = [i[0] for i in venue_get_caterer_obj_none]
        return render_template('caterer_venues.html', get_venues_for_caterer=get_venues_for_caterer,
                               caterer=current_caterer.id,
                               venue_get_caterer_obj_true_list=venue_get_caterer_obj_true_list,
                               venue_get_caterer_obj_false_list=venue_get_caterer_obj_false_list,
                               venue_get_caterer_obj_none_list=venue_get_caterer_obj_none_list)

    def get_caterer_send_request(self, venue_id, caterer_id):
        """
        caterer sends request to venue
        :param venue_id:from selected venue
        :param caterer_id:from current user's id
        :return:redirects to home template when caterer makes request
        """
        VenueGetCaterer.venue_get_caterer_query(venue_id=venue_id, caterer_id=caterer_id)
        return redirect(url_for('users.home'))

    def get_caterer_category(self):
        """
        user adds food category and it's charges and add details in CatererGetFoodCategory table
        :return:
        """
        form = CatererAddCategoryForm()
        if form.validate_on_submit():
            caterer = Caterer.get_current_caterer()
            food_category = FoodCategory.get_food_category(food_type=form.food_type.data)
            CatererGetFoodCategory.get_food_charges(caterer_id=caterer.id,
                                                    food_category_id=food_category.id,
                                                    charges=form.food_charges.data)
            return redirect(url_for('users.home'))
        return render_template('caterer_category.html', form=form, title="Caterer_category")

    def get_view_food_category(self):
        """
        caterer can view his added food category and it's charges
        :return: view_caterer_category template
        """
        caterer = Caterer.get_current_caterer()
        get_caterer = CatererGetFoodCategory.get_caterer_query(caterer_id=caterer.id)
        return render_template('view_caterer_category.html', get_caterer=get_caterer)

    def get_update_category_for_caterer(self, caterer_id, food_category_id):
        """
        caterer can update food category or it's charges
        :param caterer_id: from current user's id
        :param food_category_id: from caterer id
        :return:caterer_category template
        """
        form = CatererAddCategoryForm()
        if form.validate_on_submit():
            CatererGetFoodCategory.update_charge(caterer_id=caterer_id, food_category_id=food_category_id,
                                                 charges=form.food_charges.data)
            FoodCategory.update_category(food_category_id=food_category_id, food_category=form.food_type.data)
            return render_template('caterer_category.html', form=form)
        elif request.method == 'GET':
            charge = CatererGetFoodCategory.charge_query_for_caterer(caterer_id=caterer_id,
                                                                     food_category_id=food_category_id)
            category = FoodCategory.food_category_query(food_category_id=food_category_id)
            form.food_charges.data = charge.charges
            form.food_type.data = category.food_type
        return render_template('caterer_category.html', form=form, title="Decoration_category")

    def get_delete_category_for_caterer(self, caterer_id, food_category_id):
        """
        user can delete food category
        :param caterer_id: from current user's id
        :param food_category_id: from caterer id
        :return:view_caterer_category template
        """
        form = CatererAddCategoryForm()
        CatererGetFoodCategory.delete_charge(caterer_id=caterer_id, food_category_id=food_category_id)
        FoodCategory.delete_category(food_category_id=food_category_id)
        return render_template('view_caterer_category.html', form=form)
