from flask import render_template, url_for, redirect, request

from event_management_system.book_event.models import Event
from event_management_system.decorator.forms import AddCategoryForm
from event_management_system.decorator.models import Decorator, DecoratorType, DecoratorGetTypes
from event_management_system.venue.models import Venues, VenueGetDecorator


class DecoratorClass:
    def get_decorator_event(self):
        """
        list of events where decorator has decorated the venue
        :return:decorator_check_event template
        """
        decorator = Decorator.get_current_decorator()
        event_detail = Event.get_event_details_for_decorator(decorator_id=decorator.id)
        return render_template('decorator_check_event.html', event_detail=event_detail)

    def get_decorator_venues(self):
        """
        list of venues where decorator has requested business deal with it's status
        :return: decorator_venues template
        """
        get_venues = Venues.get_all_venues()
        current_decorator = Decorator.get_current_decorator()
        venue_get_decorator_obj_true = VenueGetDecorator.venue_get_decorator_query_for_decorator(
            decorator_id=current_decorator.id,
            is_approved_decorator=True)
        venue_get_decorator_obj_false = VenueGetDecorator.venue_get_decorator_query_for_decorator(
            decorator_id=current_decorator.id,
            is_approved_decorator=False)
        venue_get_decorator_obj_none = VenueGetDecorator.venue_get_decorator_query_for_decorator(
            decorator_id=current_decorator.id,
            is_approved_decorator=None)
        venue_get_decorator_obj_true_list = [i[0] for i in venue_get_decorator_obj_true]
        venue_get_decorator_obj_false_list = [i[0] for i in venue_get_decorator_obj_false]
        venue_get_decorator_obj_none_list = [i[0] for i in venue_get_decorator_obj_none]
        return render_template('decorator_venues.html', get_venues=get_venues,
                               decorator=current_decorator.id,
                               venue_get_decorator_obj_true_list=venue_get_decorator_obj_true_list,
                               venue_get_decorator_obj_false_list=venue_get_decorator_obj_false_list,
                               venue_get_decorator_obj_none_list=venue_get_decorator_obj_none_list)

    def get_decorator_send_request(self, venue_id, decorator_id):
        """Decorator sends request to venue for business deal"""
        VenueGetDecorator.get_venue_get_decorator_obj_for_decorator(venue_id, decorator_id)
        return redirect(url_for('users.home'))

    def get_category(self):
        """
        decorator can add decoration category and it's charges
        :return: decorator_category template
        """
        form = AddCategoryForm()
        if form.validate_on_submit():
            decorator = Decorator.get_current_decorator()
            decor_category = DecoratorType.get_decor_category(decoration_type=form.decoration_type.data)
            # print(form.decoration_type.data)
            # print(type(form.decoration_type.data))
            DecoratorGetTypes.decor_get_types(decorator.id, decor_category.id, form.category_charges.data)
            return redirect(url_for('users.home'))
        return render_template('decorator_category.html', form=form, title="Decoration_category")

    def get_update_category(self, decorator_id, decorator_type_id):
        """
        decorator can update his decoration type and charges
        :param decorator_id: from current user's id
        :param decorator_type_id: from decorator id
        :return: decorator_category template
        """
        form = AddCategoryForm()

        if form.validate_on_submit():
            DecoratorGetTypes.update_charges(decorator_id=decorator_id, decorator_type_id=decorator_type_id,
                                             decor_charge=form.category_charges.data)
            DecoratorType.update_decor_type(decorator_type_id=decorator_type_id, decor_type=form.decoration_type.data)
            return render_template('decorator_category.html', form=form)
        elif request.method == 'GET':
            charge = DecoratorGetTypes.get_decor_charges(decorator_id=decorator_id,
                                                         decoration_type_id=decorator_type_id)
            category = DecoratorType.get_decoration_category(decorator_type_id=decorator_type_id)
            form.category_charges.data = charge.charges
            form.decoration_type.data = category.decoration_type
        return render_template('decorator_category.html', form=form, title="Decoration_category")

    def get_delete_category(self, decorator_id, decorator_type_id):
        """
        decorator can delete his decoration type and charges
        :param decorator_id: from current user's id
        :param decorator_type_id: from decorator id
        :return: view_decorator_category template
        """
        form = AddCategoryForm()
        DecoratorGetTypes.delete_decor_charge(decorator_id, decorator_type_id)
        DecoratorType.delete_decor_type(decorator_type_id=decorator_type_id)
        return render_template('view_decorator_category.html', form=form)

    def get_decoration_type(self):
        """
        decorator can view his list of decoration type and charges
        :return: view_decorator_category template
        """
        decorator = Decorator.get_current_decorator()
        get_decorator = DecoratorGetTypes.get_decorator_type(decorator_id=decorator.id)
        return render_template('view_decorator_category.html', get_decorator=get_decorator)
